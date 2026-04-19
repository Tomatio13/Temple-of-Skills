"""VacantHotelSearch client and request parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import time
import re
from typing import Any

import requests

from .area_codes import AreaCodeResolver, AreaCodeSet
from .config import RakutenConfig

VACANT_HOTEL_SEARCH_URL = (
    "https://openapi.rakuten.co.jp/engine/api/Travel/VacantHotelSearch/20170426"
)


class SearchValidationError(ValueError):
    """Raised when user input is insufficient or invalid."""


class VacantSearchError(RuntimeError):
    """Raised when the vacancy search request fails."""


@dataclass(frozen=True)
class SearchRequest:
    location: str
    checkin_date: date
    checkout_date: date
    adult_count: int
    room_num: int = 1
    min_charge: int | None = None
    max_charge: int | None = None
    squeeze_conditions: tuple[str, ...] = ()
    hits: int = 10
    page: int = 1
    max_pages: int = 1
    search_pattern: int = 1


@dataclass(frozen=True)
class HotelPlan:
    hotel_no: int | None
    hotel_name: str
    hotel_information_url: str
    plan_name: str | None
    charge: int | None
    total_charge: int | None
    charge_flag: int | None
    review_average: str | None
    address1: str | None
    address2: str | None


@dataclass(frozen=True)
class VacancySearchResponse:
    request: SearchRequest
    resolved_area: AreaCodeSet
    total_count: int | None
    plans: list[HotelPlan]
    raw_payload: dict[str, Any] | None = None
    search_scope: str = "detail"
    pages_fetched: int = 1


class VacantHotelSearchClient:
    """Thin client for Rakuten Travel VacantHotelSearch."""

    def __init__(
        self,
        config: RakutenConfig,
        area_resolver: AreaCodeResolver,
        session: requests.Session | None = None,
    ) -> None:
        self._config = config
        self._area_resolver = area_resolver
        self._session = session or requests.Session()

    def search(self, request: SearchRequest) -> VacancySearchResponse:
        validate_search_request(request)
        area = self._area_resolver.resolve(request.location)
        for scope in ("detail", "small", "middle"):
            payload, plans, pages_fetched = self._collect_scope_results(request, area, scope)
            total_count = payload.get("pagingInfo", {}).get("recordCount")
            if plans:
                return VacancySearchResponse(
                    request=request,
                    resolved_area=area,
                    total_count=total_count,
                    plans=plans,
                    raw_payload=payload,
                    search_scope=scope,
                    pages_fetched=pages_fetched,
                )
        return VacancySearchResponse(
            request=request,
            resolved_area=area,
            total_count=0,
            plans=[],
            raw_payload=payload,
            search_scope="middle",
            pages_fetched=pages_fetched,
        )

    def build_params(
        self,
        request: SearchRequest,
        area: AreaCodeSet,
        scope: str = "detail",
    ) -> dict[str, Any]:
        params: dict[str, Any] = self._config.base_params()
        params.update(
            {
                "checkinDate": request.checkin_date.isoformat(),
                "checkoutDate": request.checkout_date.isoformat(),
                "adultNum": request.adult_count,
                "roomNum": request.room_num,
                "hits": request.hits,
                "page": request.page,
                "searchPattern": request.search_pattern,
                "largeClassCode": area.large_class_code,
                "middleClassCode": area.middle_class_code,
            }
        )
        if scope in {"detail", "small"}:
            params["smallClassCode"] = area.small_class_code
        if scope == "detail":
            params["detailClassCode"] = area.detail_class_code
        if request.min_charge is not None:
            params["minCharge"] = request.min_charge
        if request.max_charge is not None:
            params["maxCharge"] = request.max_charge
        if request.squeeze_conditions:
            params["squeezeCondition"] = ",".join(request.squeeze_conditions)
        return params

    def _request_payload(
        self,
        request: SearchRequest,
        area: AreaCodeSet,
        scope: str,
    ) -> dict[str, Any]:
        params = self.build_params(request, area, scope)
        response = self._get_with_retry(params)
        payload = _safe_json(response)
        if response.status_code == 404 and payload.get("error") == "not_found":
            return {"hotels": []}
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise VacantSearchError(
                _format_http_error(response.status_code, payload)
            ) from exc

        if "error" in payload or "error_description" in payload:
            raise VacantSearchError(
                f"Rakuten API error: {payload.get('error')} "
                f"{payload.get('error_description', '')}".strip()
            )
        return payload

    def _collect_scope_results(
        self,
        request: SearchRequest,
        area: AreaCodeSet,
        scope: str,
    ) -> tuple[dict[str, Any], list[HotelPlan], int]:
        payloads: list[dict[str, Any]] = []
        plans: list[HotelPlan] = []
        pages_fetched = 0
        current_page = request.page
        for _ in range(request.max_pages):
            page_request = SearchRequest(
                location=request.location,
                checkin_date=request.checkin_date,
                checkout_date=request.checkout_date,
                adult_count=request.adult_count,
                room_num=request.room_num,
                min_charge=request.min_charge,
                max_charge=request.max_charge,
                squeeze_conditions=request.squeeze_conditions,
                hits=request.hits,
                page=current_page,
                max_pages=1,
                search_pattern=request.search_pattern,
            )
            payload = self._request_payload(page_request, area, scope)
            payloads.append(payload)
            plans.extend(parse_hotels(payload))
            pages_fetched += 1
            paging = payload.get("pagingInfo") or {}
            page_count = paging.get("pageCount")
            page = paging.get("page")
            if not paging or not page_count or not page or page >= page_count:
                break
            current_page += 1
        return merge_payload_hotels(payloads), plans, pages_fetched

    def _get_with_retry(self, params: dict[str, Any]) -> requests.Response:
        last_response: requests.Response | None = None
        last_exception: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._session.get(
                    VACANT_HOTEL_SEARCH_URL,
                    params=params,
                    headers=self._config.build_headers(),
                    timeout=self._config.timeout_seconds,
                )
                last_response = response
                if response.status_code not in {429, 500, 502, 503, 504}:
                    return response
            except requests.RequestException as exc:
                last_exception = exc
                if attempt == self._config.max_retries:
                    raise VacantSearchError(f"Rakuten request failed: {exc}") from exc

            if attempt == self._config.max_retries:
                break
            time.sleep(0.5 * (2**attempt))

        if last_response is not None:
            return last_response
        if last_exception is not None:
            raise VacantSearchError(f"Rakuten request failed: {last_exception}") from last_exception
        raise VacantSearchError("Rakuten request failed before a response was received.")


def validate_search_request(request: SearchRequest) -> None:
    if not request.location.strip():
        raise SearchValidationError("location is required.")
    if request.adult_count < 1:
        raise SearchValidationError("adult_count must be >= 1.")
    if request.room_num < 1 or request.room_num > 10:
        raise SearchValidationError("room_num must be between 1 and 10.")
    if request.checkin_date >= request.checkout_date:
        raise SearchValidationError("checkout_date must be after checkin_date.")
    if request.hits < 1 or request.hits > 30:
        raise SearchValidationError("hits must be between 1 and 30.")
    if request.page < 1 or request.page > 100:
        raise SearchValidationError("page must be between 1 and 100.")
    if request.max_pages < 1 or request.max_pages > 10:
        raise SearchValidationError("max_pages must be between 1 and 10.")
    if request.search_pattern not in {0, 1}:
        raise SearchValidationError("search_pattern must be 0 or 1.")
    if request.min_charge is not None and request.min_charge < 0:
        raise SearchValidationError("min_charge must be >= 0.")
    if request.max_charge is not None and request.max_charge < 0:
        raise SearchValidationError("max_charge must be >= 0.")
    if (
        request.min_charge is not None
        and request.max_charge is not None
        and request.max_charge <= request.min_charge
    ):
        raise SearchValidationError("max_charge must be greater than min_charge.")


def parse_hotels(payload: dict[str, Any]) -> list[HotelPlan]:
    hotels = payload.get("hotels", [])
    plans: list[HotelPlan] = []
    for hotel_entry in hotels:
        sections = hotel_entry.get("hotel", [])
        merged = _merge_named_sections(sections)
        basic = merged.get("hotelBasicInfo", {})
        room_infos = _normalize_room_infos(merged.get("roomInfo"))
        if not room_infos:
            plans.append(
                HotelPlan(
                    hotel_no=_extract_hotel_no(basic),
                    hotel_name=basic.get("hotelName", ""),
                    hotel_information_url=_extract_hotel_url(basic),
                    plan_name=None,
                    charge=None,
                    total_charge=None,
                    charge_flag=None,
                    review_average=basic.get("reviewAverage"),
                    address1=basic.get("address1"),
                    address2=basic.get("address2"),
                )
            )
            continue
        for room in room_infos:
            daily_charge = room.get("dailyCharge", {})
            plan = room.get("planInfo", {})
            plans.append(
                HotelPlan(
                    hotel_no=_extract_hotel_no(basic),
                    hotel_name=basic.get("hotelName", ""),
                    hotel_information_url=_extract_hotel_url(basic),
                    plan_name=plan.get("planName"),
                    charge=daily_charge.get("rakutenCharge"),
                    total_charge=daily_charge.get("total"),
                    charge_flag=daily_charge.get("chargeFlag"),
                    review_average=basic.get("reviewAverage"),
                    address1=basic.get("address1"),
                    address2=basic.get("address2"),
                )
            )
    return plans


def merge_payload_hotels(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    if not payloads:
        return {"hotels": []}
    merged = dict(payloads[-1])
    hotels: list[Any] = []
    for payload in payloads:
        hotels.extend(payload.get("hotels", []))
    merged["hotels"] = hotels
    first_paging = payloads[0].get("pagingInfo", {})
    last_paging = payloads[-1].get("pagingInfo", {})
    if first_paging or last_paging:
        merged["pagingInfo"] = {
            "recordCount": first_paging.get("recordCount", last_paging.get("recordCount")),
            "pageCount": first_paging.get("pageCount", last_paging.get("pageCount")),
            "page": first_paging.get("page", 1),
            "first": first_paging.get("first", 1),
            "last": last_paging.get("last", first_paging.get("last")),
        }
    return merged


def parse_natural_language_request(text: str) -> SearchRequest:
    location = _extract_location(text)
    checkin_date = _extract_date(text, "checkin")
    checkout_date = _extract_date(text, "checkout")
    adult_count = _extract_count(text, r"(\d+)\s*名")
    room_num = _extract_optional_count(text, r"(\d+)\s*室", default=1)
    min_charge = _extract_optional_count(text, r"最低\s*(\d+)\s*円", default=None)
    max_charge = _extract_optional_count(text, r"最大\s*(\d+)\s*円", default=None)
    squeeze_conditions: list[str] = []
    if "禁煙" in text:
        squeeze_conditions.append("kinen")
    if "朝食" in text:
        squeeze_conditions.append("breakfast")
    if "夕食" in text:
        squeeze_conditions.append("dinner")
    if "温泉" in text:
        squeeze_conditions.append("onsen")
    return SearchRequest(
        location=location,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        adult_count=adult_count,
        room_num=room_num,
        min_charge=min_charge,
        max_charge=max_charge,
        squeeze_conditions=tuple(squeeze_conditions),
    )


def missing_fields_from_text(text: str) -> list[str]:
    missing: list[str] = []
    if not _safe_extract(lambda: _extract_location(text)):
        missing.append("location")
    if not _safe_extract(lambda: _extract_date(text, "checkin")):
        missing.append("checkin_date")
    if not _safe_extract(lambda: _extract_date(text, "checkout")):
        missing.append("checkout_date")
    if not _safe_extract(lambda: _extract_count(text, r"(\d+)\s*名")):
        missing.append("adult_count")
    return missing


def _safe_extract(fn: Any) -> bool:
    try:
        fn()
        return True
    except SearchValidationError:
        return False


def _extract_location(text: str) -> str:
    match = re.search(r"(.+?)で", text)
    if not match:
        raise SearchValidationError("location is missing from the input text.")
    return match.group(1).strip(" 、,")


def _extract_date(text: str, label: str) -> date:
    keyword = "チェックイン" if label == "checkin" else "チェックアウト"
    match = re.search(r"(\d{4}-\d{2}-\d{2})\s*" + keyword, text)
    if not match:
        raise SearchValidationError(f"{label}_date is missing from the input text.")
    return datetime.strptime(match.group(1), "%Y-%m-%d").date()


def _extract_count(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    if not match:
        raise SearchValidationError("required numeric field is missing from the input text.")
    return int(match.group(1))


def _extract_optional_count(text: str, pattern: str, default: int | None) -> int | None:
    match = re.search(pattern, text)
    if not match:
        return default
    return int(match.group(1))


def _merge_named_sections(sections: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for section in sections:
        for key, value in section.items():
            merged[key] = value
    return merged


def _normalize_room_infos(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        if all(isinstance(item, dict) and _looks_like_room_fragment(item) for item in value):
            merged: dict[str, Any] = {}
            for item in value:
                merged.update(item)
            return [merged] if merged else []

        normalized: list[dict[str, Any]] = []
        for item in value:
            if isinstance(item, dict) and _looks_like_full_room_info(item):
                normalized.append(item)
                continue
            if isinstance(item, dict):
                merged: dict[str, Any] = {}
                for key, nested in item.items():
                    merged[key] = nested
                if merged:
                    normalized.append(merged)
        return normalized
    return []


def _looks_like_room_fragment(item: dict[str, Any]) -> bool:
    room_keys = {"roomBasicInfo", "dailyCharge", "planInfo", "reserveUrl"}
    return any(key in room_keys for key in item)


def _looks_like_full_room_info(item: dict[str, Any]) -> bool:
    return "dailyCharge" in item or "planInfo" in item or "roomBasicInfo" in item


def summarize_hotels(plans: list[HotelPlan], limit: int = 10) -> list[HotelPlan]:
    grouped: dict[tuple[int | None, str, str], HotelPlan] = {}
    for plan in plans:
        key = (plan.hotel_no, plan.hotel_name, plan.hotel_information_url)
        current = grouped.get(key)
        if current is None:
            grouped[key] = plan
            continue
        grouped[key] = _pick_better_plan(current, plan)

    ordered = sorted(
        grouped.values(),
        key=lambda item: (
            _sort_charge(item) >= 10**12,
            _sort_charge(item),
            item.hotel_name,
        ),
    )
    return ordered[:limit]


def _pick_better_plan(left: HotelPlan, right: HotelPlan) -> HotelPlan:
    left_charge = _sort_charge(left)
    right_charge = _sort_charge(right)
    if right_charge < left_charge:
        return right
    if right_charge == left_charge and (right.plan_name or "") < (left.plan_name or ""):
        return right
    return left


def _sort_charge(plan: HotelPlan) -> int:
    if plan.total_charge is not None:
        return plan.total_charge
    if plan.charge is not None:
        return plan.charge
    return 10**12


def _extract_hotel_url(basic: dict[str, Any]) -> str:
    for key in ("hotelInformationUrl", "hotelInformationUrlMobile", "hotelSpecialUrl"):
        value = basic.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _extract_hotel_no(basic: dict[str, Any]) -> int | None:
    value = basic.get("hotelNo")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _safe_json(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise VacantSearchError("Rakuten VacantHotelSearch returned invalid JSON.") from exc
    if isinstance(payload, dict):
        return payload
    raise VacantSearchError("Rakuten VacantHotelSearch returned an unexpected payload.")


def _format_http_error(status_code: int, payload: dict[str, Any]) -> str:
    error = payload.get("error")
    description = payload.get("error_description")
    if error or description:
        joined = " ".join(part for part in [str(error or "").strip(), str(description or "").strip()] if part)
        return f"Rakuten VacantHotelSearch failed with HTTP {status_code}: {joined}"
    return f"Rakuten VacantHotelSearch failed with HTTP {status_code}."

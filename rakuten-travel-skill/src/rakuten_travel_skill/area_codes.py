"""Area code resolution using Rakuten GetAreaClass."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

import requests

from .config import RakutenConfig

AREA_CLASS_URL = "https://openapi.rakuten.co.jp/engine/api/Travel/GetAreaClass/20131024"


class AreaCodeError(RuntimeError):
    """Raised when area code resolution fails."""


@dataclass(frozen=True)
class AreaCodeSet:
    large_class_code: str
    large_class_name: str
    middle_class_code: str
    middle_class_name: str
    small_class_code: str
    small_class_name: str
    detail_class_code: str
    detail_class_name: str


class AreaCodeResolver:
    """Resolve natural-language locations to Rakuten travel area codes."""

    def __init__(
        self,
        config: RakutenConfig,
        session: requests.Session | None = None,
    ) -> None:
        self._config = config
        self._session = session or requests.Session()
        self._cache: list[AreaCodeSet] | None = None

    def load_area_codes(self, refresh: bool = False) -> list[AreaCodeSet]:
        if self._cache is not None and not refresh:
            return self._cache

        if not refresh:
            cached = self._load_from_disk()
            if cached is not None:
                self._cache = cached
                return cached

        payload = self._request_area_classes()
        area_codes = flatten_area_classes(payload)
        self._cache = area_codes
        self._save_to_disk(area_codes)
        return area_codes

    def resolve(self, location: str) -> AreaCodeSet:
        normalized_query = normalize_location(location)
        matches = self.find_candidates(normalized_query)

        exact_matches = [
            item
            for item in matches
            if normalized_query
            in {
                normalize_location(item.detail_class_name),
                normalize_location(item.small_class_name),
                normalize_location(item.middle_class_name),
            }
        ]
        if len(exact_matches) == 1:
            return exact_matches[0]
        if len(exact_matches) > 1:
            raise AreaCodeError(_format_candidates(location, exact_matches))

        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise AreaCodeError(
                f"'{location}' に一致する楽天トラベル地区コードが見つかりませんでした。"
            )
        raise AreaCodeError(_format_candidates(location, matches))

    def find_candidates(self, location: str) -> list[AreaCodeSet]:
        query = normalize_location(location)
        if not query:
            raise AreaCodeError("場所が空です。地区コードを解決できません。")

        matches: list[AreaCodeSet] = []
        for area in self.load_area_codes():
            names = (
                normalize_location(area.detail_class_name),
                normalize_location(area.small_class_name),
                normalize_location(area.middle_class_name),
                normalize_location(area.large_class_name),
            )
            if any(query == name for name in names):
                matches.append(area)

        if matches:
            return _dedupe(matches)

        for area in self.load_area_codes():
            names = (
                normalize_location(area.detail_class_name),
                normalize_location(area.small_class_name),
                normalize_location(area.middle_class_name),
                normalize_location(area.large_class_name),
            )
            if any(query in name or name in query for name in names if name):
                matches.append(area)
        return _dedupe(matches)

    def _request_area_classes(self) -> dict[str, Any]:
        response = self._session.get(
            AREA_CLASS_URL,
            params=self._config.base_params(),
            headers=self._config.build_headers(),
            timeout=self._config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def _load_from_disk(self) -> list[AreaCodeSet] | None:
        path = self._config.area_cache_path
        if not path or not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            raw_items = json.load(handle)
        return [AreaCodeSet(**item) for item in raw_items]

    def _save_to_disk(self, area_codes: list[AreaCodeSet]) -> None:
        path = self._config.area_cache_path
        if not path:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump([asdict(item) for item in area_codes], handle, ensure_ascii=False, indent=2)


def normalize_location(value: str) -> str:
    return (
        value.strip()
        .replace("　", "")
        .replace(" ", "")
        .replace("都", "")
        .replace("道", "")
        .replace("府", "")
        .replace("県", "")
        .replace("市", "")
        .replace("区", "")
        .lower()
    )


def flatten_area_classes(payload: dict[str, Any]) -> list[AreaCodeSet]:
    try:
        large_classes = payload["areaClasses"]["largeClasses"]
    except KeyError as exc:
        raise AreaCodeError("GetAreaClass response is missing areaClasses.largeClasses.") from exc

    items: list[AreaCodeSet] = []
    for large_entry in large_classes:
        large_node = _extract_named_node(large_entry, "largeClass")
        large_code = _node_value(large_node, "code", "largeClassCode")
        large_name = _node_value(large_node, "name", "largeClassName")
        middle_classes = _child_list(large_node, "middleClasses")
        for middle_entry in middle_classes:
            middle_node = _extract_named_node(middle_entry, "middleClass")
            middle_code = _node_value(middle_node, "code", "middleClassCode")
            middle_name = _node_value(middle_node, "name", "middleClassName")
            small_classes = _child_list(middle_node, "smallClasses")
            for small_entry in small_classes:
                small_node = _extract_named_node(small_entry, "smallClass")
                small_code = _node_value(small_node, "code", "smallClassCode")
                small_name = _node_value(small_node, "name", "smallClassName")
                detail_classes = _child_list(small_node, "detailClasses")
                if not detail_classes:
                    items.append(
                        AreaCodeSet(
                            large_class_code=large_code,
                            large_class_name=large_name,
                            middle_class_code=middle_code,
                            middle_class_name=middle_name,
                            small_class_code=small_code,
                            small_class_name=small_name,
                            detail_class_code=small_code,
                            detail_class_name=small_name,
                        )
                    )
                    continue
                for detail_entry in detail_classes:
                    detail_node = _extract_named_node(detail_entry, "detailClass")
                    items.append(
                        AreaCodeSet(
                            large_class_code=large_code,
                            large_class_name=large_name,
                            middle_class_code=middle_code,
                            middle_class_name=middle_name,
                            small_class_code=small_code,
                            small_class_name=small_name,
                            detail_class_code=_node_value(detail_node, "code", "detailClassCode"),
                            detail_class_name=_node_value(detail_node, "name", "detailClassName"),
                        )
                    )
    return items


def _extract_named_node(entry: dict[str, Any], key: str) -> dict[str, Any]:
    value = entry[key]
    if isinstance(value, list):
        merged: dict[str, Any] = {}
        for item in value:
            if isinstance(item, dict):
                merged.update(item)
        return merged
    return value


def _node_value(node: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = node.get(key)
        if isinstance(value, str):
            return value
    raise AreaCodeError(f"Missing keys {keys} in GetAreaClass response node.")


def _child_list(node: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = node.get(key, [])
    if isinstance(value, list):
        return value
    return []


def _format_candidates(location: str, candidates: list[AreaCodeSet]) -> str:
    lines = [f"'{location}' は複数の地区候補に一致しました。候補を絞ってください。"]
    for item in candidates[:10]:
        lines.append(
            f"- {item.large_class_name} / {item.middle_class_name} / "
            f"{item.small_class_name} / {item.detail_class_name}"
        )
    return "\n".join(lines)


def _dedupe(items: list[AreaCodeSet]) -> list[AreaCodeSet]:
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[AreaCodeSet] = []
    for item in items:
        key = (
            item.large_class_code,
            item.middle_class_code,
            item.small_class_code,
            item.detail_class_code,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped

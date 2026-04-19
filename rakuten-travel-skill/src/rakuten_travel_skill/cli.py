"""CLI entrypoint for Rakuten Travel vacancy search skill."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from .area_codes import AreaCodeError, AreaCodeResolver
from .config import ConfigError, RakutenConfig
from .formatter import format_error, format_search_response
from .vacant_search import (
    SearchRequest,
    SearchValidationError,
    VacantHotelSearchClient,
    VacantSearchError,
    missing_fields_from_text,
    parse_natural_language_request,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rakuten Travel vacancy search skill")
    parser.add_argument("text", nargs="?", help="Natural language travel request")
    parser.add_argument("--json", dest="json_payload", help="Search request JSON string")
    parser.add_argument("--page", type=int, help="Result page number (1-100)")
    parser.add_argument("--max-pages", type=int, help="Fetch multiple pages starting from --page")
    parser.add_argument("--hits", type=int, help="Results per page (1-30)")
    parser.add_argument(
        "--search-pattern",
        type=int,
        choices=[0, 1],
        help="0: hotel summary, 1: plan-based search",
    )
    parser.add_argument("--room-num", type=int, help="Number of rooms")
    parser.add_argument("--min-charge", type=int, help="Minimum nightly charge in JPY")
    parser.add_argument("--max-charge", type=int, help="Maximum nightly charge in JPY")
    parser.add_argument("--refresh-area-cache", action="store_true")
    parser.add_argument("--debug", action="store_true", help="Print request/response debug info")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = RakutenConfig.from_env()
        resolver = AreaCodeResolver(config)
        if args.refresh_area_cache:
            resolver.load_area_codes(refresh=True)
        request = _build_request(args)
        client = VacantHotelSearchClient(config, resolver)
        result = client.search(request)
        if args.debug or os.getenv("RAKUTEN_DEBUG") == "1":
            print(_format_debug(result), file=sys.stderr)
        print(format_search_response(result))
        return 0
    except ConfigError as exc:
        print(format_error(str(exc), retryable=False), file=sys.stderr)
        return 2
    except SearchValidationError as exc:
        print(format_error(str(exc), retryable=False), file=sys.stderr)
        return 2
    except AreaCodeError as exc:
        print(format_error(str(exc), retryable=False), file=sys.stderr)
        return 3
    except VacantSearchError as exc:
        print(format_error(str(exc), retryable=True), file=sys.stderr)
        return 4


def _build_request(args: argparse.Namespace) -> SearchRequest:
    if args.json_payload:
        payload = json.loads(args.json_payload)
        return _apply_cli_overrides(SearchRequest(**_normalize_json_payload(payload)), args)
    if not args.text:
        raise SearchValidationError(
            "検索条件がありません。自然文か --json で入力してください。"
        )
    missing = missing_fields_from_text(args.text)
    if missing:
        raise SearchValidationError(
            "必須項目が不足しています: " + ", ".join(_field_label(name) for name in missing)
        )
    return _apply_cli_overrides(parse_natural_language_request(args.text), args)


def _normalize_json_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for key in ("checkin_date", "checkout_date"):
        if key in normalized and isinstance(normalized[key], str):
            from datetime import datetime

            normalized[key] = datetime.strptime(normalized[key], "%Y-%m-%d").date()
    if "squeeze_conditions" in normalized and isinstance(normalized["squeeze_conditions"], list):
        normalized["squeeze_conditions"] = tuple(normalized["squeeze_conditions"])
    return normalized


def _field_label(name: str) -> str:
    labels = {
        "location": "場所",
        "checkin_date": "チェックイン日",
        "checkout_date": "チェックアウト日",
        "adult_count": "人数",
    }
    return labels.get(name, name)


def _apply_cli_overrides(request: SearchRequest, args: argparse.Namespace) -> SearchRequest:
    values = {
        "page": args.page if args.page is not None else request.page,
        "max_pages": args.max_pages if args.max_pages is not None else request.max_pages,
        "hits": args.hits if args.hits is not None else request.hits,
        "search_pattern": (
            args.search_pattern if args.search_pattern is not None else request.search_pattern
        ),
        "room_num": args.room_num if args.room_num is not None else request.room_num,
        "min_charge": args.min_charge if args.min_charge is not None else request.min_charge,
        "max_charge": args.max_charge if args.max_charge is not None else request.max_charge,
    }
    return SearchRequest(
        location=request.location,
        checkin_date=request.checkin_date,
        checkout_date=request.checkout_date,
        adult_count=request.adult_count,
        room_num=values["room_num"],
        min_charge=values["min_charge"],
        max_charge=values["max_charge"],
        squeeze_conditions=request.squeeze_conditions,
        hits=values["hits"],
        page=values["page"],
        max_pages=values["max_pages"],
        search_pattern=values["search_pattern"],
    )


def _format_debug(result) -> str:
    payload = result.raw_payload or {}
    hotel_count = len(payload.get("hotels", [])) if isinstance(payload, dict) else "unknown"
    paging = payload.get("pagingInfo") if isinstance(payload, dict) else None
    return "\n".join(
        [
            "[debug] request",
            f"location={result.request.location}",
            (
                "resolved_area="
                f"{result.resolved_area.large_class_code}/"
                f"{result.resolved_area.middle_class_code}/"
                f"{result.resolved_area.small_class_code}/"
                f"{result.resolved_area.detail_class_code}"
            ),
            f"search_scope={result.search_scope}",
            (
                "dates="
                f"{result.request.checkin_date.isoformat()}.."
                f"{result.request.checkout_date.isoformat()}"
            ),
            f"adults={result.request.adult_count} rooms={result.request.room_num}",
            f"pages_fetched={result.pages_fetched}",
            f"payload_hotels={hotel_count}",
            f"payload_paging={paging}",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())

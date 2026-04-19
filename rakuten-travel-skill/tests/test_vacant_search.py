from datetime import date
import argparse
import unittest

from rakuten_travel_skill.area_codes import AreaCodeSet
from rakuten_travel_skill.config import RakutenConfig
from rakuten_travel_skill.cli import _apply_cli_overrides
from rakuten_travel_skill.vacant_search import (
    SearchRequest,
    SearchValidationError,
    VacantHotelSearchClient,
    HotelPlan,
    merge_payload_hotels,
    missing_fields_from_text,
    parse_hotels,
    parse_natural_language_request,
    summarize_hotels,
    validate_search_request,
)


class StubResolver:
    def resolve(self, location: str) -> AreaCodeSet:
        return AreaCodeSet(
            large_class_code="japan",
            large_class_name="日本",
            middle_class_code="kyoto",
            middle_class_name="京都府",
            small_class_code="shi",
            small_class_name="京都市内",
            detail_class_code="A",
            detail_class_name="京都駅",
        )


class DummyResponse:
    def __init__(self, payload, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            import requests

            raise requests.HTTPError(response=self)

    def json(self):
        return self._payload


class DummySession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, params, headers, timeout):
        self.calls.append((url, params, headers, timeout))
        return DummyResponse(self.payload)


class SequencedStatusSession:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, params, headers, timeout):
        self.calls.append((url, params, headers, timeout))
        payload, status = self.responses[len(self.calls) - 1]
        return DummyResponse(payload, status_code=status)


class VacantSearchTest(unittest.TestCase):
    def test_cli_overrides_request(self) -> None:
        request = SearchRequest(
            location="館山",
            checkin_date=date(2026, 5, 8),
            checkout_date=date(2026, 5, 9),
            adult_count=2,
        )
        args = argparse.Namespace(
            page=2,
            max_pages=3,
            hits=30,
            search_pattern=0,
            room_num=2,
            min_charge=10000,
            max_charge=25000,
        )
        updated = _apply_cli_overrides(request, args)
        self.assertEqual(updated.page, 2)
        self.assertEqual(updated.max_pages, 3)
        self.assertEqual(updated.hits, 30)
        self.assertEqual(updated.search_pattern, 0)
        self.assertEqual(updated.room_num, 2)
        self.assertEqual(updated.min_charge, 10000)
        self.assertEqual(updated.max_charge, 25000)

    def test_validate_request(self) -> None:
        request = SearchRequest(
            location="京都市",
            checkin_date=date(2026, 5, 1),
            checkout_date=date(2026, 5, 2),
            adult_count=2,
        )
        validate_search_request(request)

    def test_validate_rejects_bad_hits(self) -> None:
        request = SearchRequest(
            location="京都市",
            checkin_date=date(2026, 5, 1),
            checkout_date=date(2026, 5, 2),
            adult_count=2,
            hits=31,
        )
        with self.assertRaises(SearchValidationError):
            validate_search_request(request)

    def test_parse_natural_language_request(self) -> None:
        request = parse_natural_language_request(
            "京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名 禁煙 朝食"
        )
        self.assertEqual(request.location, "京都市")
        self.assertEqual(request.adult_count, 2)
        self.assertIn("kinen", request.squeeze_conditions)
        self.assertIn("breakfast", request.squeeze_conditions)

    def test_missing_fields_detection(self) -> None:
        self.assertEqual(
            missing_fields_from_text("京都市で2026-05-01チェックイン"),
            ["checkout_date", "adult_count"],
        )

    def test_build_and_parse_search_response(self) -> None:
        payload = {
            "pagingInfo": {"recordCount": 1},
            "hotels": [
                {
                    "hotel": [
                        {
                            "hotelBasicInfo": {
                                "hotelName": "京都ホテル",
                                "hotelInformationUrl": "https://example.com/hotel",
                                "reviewAverage": "4.2",
                                "address1": "京都府",
                                "address2": "京都市",
                            }
                        },
                        {
                            "roomInfo": [
                                {"roomBasicInfo": {"roomName": "ツイン"}},
                                {"dailyCharge": {"rakutenCharge": 18000}},
                                {"planInfo": {"planName": "朝食付き"}},
                            ]
                        },
                    ]
                }
            ],
        }
        session = DummySession(payload)
        client = VacantHotelSearchClient(
            RakutenConfig(application_id="app"),
            StubResolver(),
            session=session,
        )
        response = client.search(
            SearchRequest(
                location="京都市",
                checkin_date=date(2026, 5, 1),
                checkout_date=date(2026, 5, 2),
                adult_count=2,
            )
        )
        self.assertEqual(response.total_count, 1)
        self.assertEqual(response.plans[0].hotel_name, "京都ホテル")
        self.assertEqual(session.calls[0][1]["detailClassCode"], "A")
        self.assertEqual(response.search_scope, "detail")
        self.assertEqual(response.pages_fetched, 1)

    def test_parse_hotels(self) -> None:
        plans = parse_hotels({"hotels": [{"hotel": [{"hotelBasicInfo": {"hotelName": "A"}}]}]})
        self.assertEqual(plans[0].hotel_name, "A")

    def test_parse_hotels_with_room_info_list(self) -> None:
        plans = parse_hotels(
            {
                "hotels": [
                    {
                        "hotel": [
                            {"hotelBasicInfo": {"hotelName": "A"}},
                            {
                                "roomInfo": [
                                    {"roomBasicInfo": {"roomName": "ツイン"}},
                                    {"dailyCharge": {"rakutenCharge": 9000}},
                                    {"planInfo": {"planName": "素泊まり"}},
                                ]
                            },
                        ]
                    }
                ]
            }
        )
        self.assertEqual(plans[0].charge, 9000)
        self.assertEqual(plans[0].plan_name, "素泊まり")
        self.assertEqual(plans[0].hotel_no, None)
        self.assertEqual(plans[0].total_charge, None)

    def test_404_not_found_becomes_empty_result(self) -> None:
        session = DummySession({"error": "not_found", "error_description": "not found"})
        session.get = lambda url, params, headers, timeout: DummyResponse(
            {"error": "not_found", "error_description": "not found"},
            status_code=404,
        )
        client = VacantHotelSearchClient(
            RakutenConfig(application_id="app"),
            StubResolver(),
            session=session,
        )
        response = client.search(
            SearchRequest(
                location="館山",
                checkin_date=date(2026, 5, 1),
                checkout_date=date(2026, 5, 2),
                adult_count=3,
            )
        )
        self.assertEqual(response.total_count, 0)
        self.assertEqual(response.plans, [])

    def test_search_falls_back_to_wider_scope(self) -> None:
        payloads = [
            {"hotels": []},
            {"hotels": []},
            {
                "pagingInfo": {"recordCount": 1},
                "hotels": [
                    {
                        "hotel": [
                            {"hotelBasicInfo": {"hotelName": "館山ホテル"}},
                            {
                                "roomInfo": [
                                    {"dailyCharge": {"rakutenCharge": 12000}},
                                    {"planInfo": {"planName": "素泊まり"}},
                                ]
                            },
                        ]
                    }
                ],
            },
        ]

        class SequencedSession:
            def __init__(self, responses):
                self.responses = responses
                self.calls = []

            def get(self, url, params, headers, timeout):
                self.calls.append(params.copy())
                return DummyResponse(self.responses[len(self.calls) - 1])

        session = SequencedSession(payloads)
        client = VacantHotelSearchClient(
            RakutenConfig(application_id="app"),
            StubResolver(),
            session=session,
        )
        response = client.search(
            SearchRequest(
                location="館山",
                checkin_date=date(2026, 5, 8),
                checkout_date=date(2026, 5, 9),
                adult_count=2,
            )
        )
        self.assertEqual(response.search_scope, "middle")
        self.assertEqual(response.plans[0].hotel_name, "館山ホテル")
        self.assertIn("detailClassCode", session.calls[0])
        self.assertIn("smallClassCode", session.calls[1])
        self.assertNotIn("detailClassCode", session.calls[1])
        self.assertNotIn("smallClassCode", session.calls[2])

    def test_retries_on_429(self) -> None:
        session = SequencedStatusSession(
            [
                ({"error": "too_many_requests"}, 429),
                (
                    {
                        "pagingInfo": {"recordCount": 1},
                        "hotels": [
                            {
                                "hotel": [
                                    {"hotelBasicInfo": {"hotelName": "館山ホテル"}},
                                    {
                                        "roomInfo": [
                                            {"dailyCharge": {"rakutenCharge": 12000}},
                                            {"planInfo": {"planName": "素泊まり"}},
                                        ]
                                    },
                                ]
                            }
                        ],
                    },
                    200,
                ),
            ]
        )
        client = VacantHotelSearchClient(
            RakutenConfig(application_id="app", max_retries=1),
            StubResolver(),
            session=session,
        )
        response = client.search(
            SearchRequest(
                location="館山",
                checkin_date=date(2026, 5, 8),
                checkout_date=date(2026, 5, 9),
                adult_count=2,
            )
        )
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(response.plans[0].hotel_name, "館山ホテル")

    def test_summarize_hotels_keeps_lowest_price_per_hotel(self) -> None:
        summarized = summarize_hotels(
            [
                HotelPlan(
                    hotel_no=1,
                    hotel_name="Aホテル",
                    hotel_information_url="https://example.com/a",
                    plan_name="朝食付き",
                    charge=12000,
                    total_charge=24000,
                    charge_flag=0,
                    review_average="4.0",
                    address1="千葉県",
                    address2="館山市",
                ),
                HotelPlan(
                    hotel_no=1,
                    hotel_name="Aホテル",
                    hotel_information_url="https://example.com/a",
                    plan_name="素泊まり",
                    charge=9000,
                    total_charge=18000,
                    charge_flag=0,
                    review_average="4.0",
                    address1="千葉県",
                    address2="館山市",
                ),
                HotelPlan(
                    hotel_no=2,
                    hotel_name="Bホテル",
                    hotel_information_url="https://example.com/b",
                    plan_name="素泊まり",
                    charge=10000,
                    total_charge=10000,
                    charge_flag=1,
                    review_average="4.2",
                    address1="千葉県",
                    address2="南房総市",
                ),
            ]
        )
        self.assertEqual(len(summarized), 2)
        self.assertEqual(summarized[0].hotel_name, "Bホテル")
        self.assertEqual(summarized[1].hotel_name, "Aホテル")
        self.assertEqual(summarized[1].total_charge, 18000)

    def test_merge_payload_hotels(self) -> None:
        merged = merge_payload_hotels(
            [
                {
                    "pagingInfo": {"recordCount": 25, "pageCount": 3, "page": 1, "first": 1, "last": 10},
                    "hotels": [{"hotel": []}],
                },
                {
                    "pagingInfo": {"recordCount": 25, "pageCount": 3, "page": 2, "first": 11, "last": 20},
                    "hotels": [{"hotel": []}],
                },
            ]
        )
        self.assertEqual(len(merged["hotels"]), 2)
        self.assertEqual(merged["pagingInfo"]["first"], 1)
        self.assertEqual(merged["pagingInfo"]["last"], 20)

    def test_fetches_multiple_pages(self) -> None:
        payloads = [
            (
                {
                    "pagingInfo": {"recordCount": 25, "pageCount": 3, "page": 1, "first": 1, "last": 2},
                    "hotels": [
                        {"hotel": [{"hotelBasicInfo": {"hotelName": "A", "hotelNo": 1}}]},
                        {"hotel": [{"hotelBasicInfo": {"hotelName": "B", "hotelNo": 2}}]},
                    ],
                },
                200,
            ),
            (
                {
                    "pagingInfo": {"recordCount": 25, "pageCount": 3, "page": 2, "first": 3, "last": 4},
                    "hotels": [
                        {"hotel": [{"hotelBasicInfo": {"hotelName": "C", "hotelNo": 3}}]},
                        {"hotel": [{"hotelBasicInfo": {"hotelName": "D", "hotelNo": 4}}]},
                    ],
                },
                200,
            ),
        ]
        session = SequencedStatusSession(payloads)
        client = VacantHotelSearchClient(
            RakutenConfig(application_id="app"),
            StubResolver(),
            session=session,
        )
        response = client.search(
            SearchRequest(
                location="館山",
                checkin_date=date(2026, 5, 8),
                checkout_date=date(2026, 5, 9),
                adult_count=2,
                hits=2,
                max_pages=2,
            )
        )
        self.assertEqual(response.pages_fetched, 2)
        self.assertEqual(len(response.plans), 4)
        self.assertEqual(response.raw_payload["pagingInfo"]["last"], 4)

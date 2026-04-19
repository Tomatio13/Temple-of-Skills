from datetime import date
import unittest

from rakuten_travel_skill.area_codes import AreaCodeSet
from rakuten_travel_skill.formatter import format_error, format_search_response
from rakuten_travel_skill.vacant_search import HotelPlan, SearchRequest, VacancySearchResponse


class FormatterTest(unittest.TestCase):
    def test_format_search_response(self) -> None:
        response = VacancySearchResponse(
            request=SearchRequest(
                location="京都市",
                checkin_date=date(2026, 5, 1),
                checkout_date=date(2026, 5, 2),
                adult_count=2,
            ),
            resolved_area=AreaCodeSet(
                large_class_code="japan",
                large_class_name="日本",
                middle_class_code="kyoto",
                middle_class_name="京都府",
                small_class_code="shi",
                small_class_name="京都市内",
                detail_class_code="A",
                detail_class_name="京都駅",
            ),
            total_count=1,
            plans=[
                HotelPlan(
                    hotel_no=1,
                    hotel_name="京都ホテル",
                    hotel_information_url="https://example.com",
                    plan_name="朝食付き",
                    charge=18000,
                    total_charge=36000,
                    charge_flag=0,
                    review_average="4.2",
                    address1="京都府",
                    address2="京都市",
                )
            ],
            raw_payload=None,
            search_scope="middle",
            pages_fetched=2,
        )
        text = format_search_response(response)
        self.assertIn("検索条件の確認", text)
        self.assertIn("件数情報", text)
        self.assertIn("取得ページ数", text)
        self.assertIn("京都ホテル", text)
        self.assertIn("18000円/人 (合計 36000円)", text)
        self.assertIn("検索範囲", text)

    def test_format_error(self) -> None:
        text = format_error("bad request", retryable=False)
        self.assertIn("入力修正が必要", text)

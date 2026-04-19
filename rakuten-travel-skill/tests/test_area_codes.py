import unittest

from rakuten_travel_skill.area_codes import AreaCodeError, AreaCodeResolver, flatten_area_classes
from rakuten_travel_skill.config import RakutenConfig


SAMPLE_PAYLOAD = {
    "areaClasses": {
        "largeClasses": [
            {
                "largeClass": {
                    "code": "japan",
                    "name": "日本",
                    "middleClasses": [
                        {
                            "middleClass": {
                                "code": "hokkaido",
                                "name": "北海道",
                                "smallClasses": [
                                    {
                                        "smallClass": {
                                            "code": "hakodate-area",
                                            "name": "函館・大沼・松前",
                                            "detailClasses": [
                                                {"detailClass": {"code": "hakodate", "name": "函館"}},
                                                {"detailClass": {"code": "onuma", "name": "大沼"}},
                                            ],
                                        }
                                    }
                                ],
                            }
                        }
                    ],
                }
            }
        ]
    }
}


class AreaCodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = AreaCodeResolver.__new__(AreaCodeResolver)
        self.resolver._config = RakutenConfig(application_id="app")
        self.resolver._session = None
        self.resolver._cache = flatten_area_classes(SAMPLE_PAYLOAD)

    def test_flatten_area_classes(self) -> None:
        areas = flatten_area_classes(SAMPLE_PAYLOAD)
        self.assertEqual(len(areas), 2)
        self.assertEqual(areas[0].detail_class_code, "hakodate")

    def test_resolve_exact_match(self) -> None:
        area = self.resolver.resolve("函館市")
        self.assertEqual(area.detail_class_code, "hakodate")

    def test_resolve_multiple_candidates_raises(self) -> None:
        with self.assertRaises(AreaCodeError):
            self.resolver.resolve("大")

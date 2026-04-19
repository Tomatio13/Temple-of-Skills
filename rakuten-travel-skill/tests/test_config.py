import os
import unittest
from unittest import mock

from rakuten_travel_skill.config import ConfigError, RakutenConfig


class ConfigTest(unittest.TestCase):
    def test_missing_application_id_raises(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError):
                RakutenConfig.from_env()

    def test_loads_values_from_env(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "RAKUTEN_APPLICATION_ID": "app-123",
                "RAKUTEN_ACCESS_KEY": "access-xyz",
                "RAKUTEN_AFFILIATE_ID": "aff-456",
                "RAKUTEN_TIMEOUT_SECONDS": "12",
                "RAKUTEN_MAX_RETRIES": "3",
                "RAKUTEN_USER_AGENT": "custom-agent",
                "RAKUTEN_AREA_CACHE_PATH": "/tmp/areas.json",
            },
            clear=True,
        ):
            config = RakutenConfig.from_env()

        self.assertEqual(config.application_id, "app-123")
        self.assertEqual(config.access_key, "access-xyz")
        self.assertEqual(config.affiliate_id, "aff-456")
        self.assertEqual(config.timeout_seconds, 12.0)
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.user_agent, "custom-agent")
        self.assertEqual(config.area_cache_path, "/tmp/areas.json")
        self.assertIn("applicationId", config.base_params())
        self.assertIn("accessKey", config.base_params())
        self.assertIn("Authorization", config.build_headers())

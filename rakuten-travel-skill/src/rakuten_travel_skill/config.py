"""Configuration helpers for Rakuten Travel skill."""

from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigError(ValueError):
    """Raised when the runtime configuration is invalid."""


@dataclass(frozen=True)
class RakutenConfig:
    application_id: str
    access_key: str | None = None
    affiliate_id: str | None = None
    timeout_seconds: float = 10.0
    max_retries: int = 2
    user_agent: str = "rakuten-travel-skill/0.1"
    area_cache_path: str | None = None

    @classmethod
    def from_env(cls) -> "RakutenConfig":
        application_id = os.getenv("RAKUTEN_APPLICATION_ID", "").strip()
        if not application_id:
            raise ConfigError(
                "RAKUTEN_APPLICATION_ID is required. "
                "Set it before running the Rakuten Travel skill."
            )

        access_key = os.getenv("RAKUTEN_ACCESS_KEY", "").strip() or None
        affiliate_id = os.getenv("RAKUTEN_AFFILIATE_ID", "").strip() or None
        timeout_seconds = _read_float("RAKUTEN_TIMEOUT_SECONDS", default=10.0, minimum=1.0)
        max_retries = _read_int("RAKUTEN_MAX_RETRIES", default=2, minimum=0)
        user_agent = os.getenv("RAKUTEN_USER_AGENT", "rakuten-travel-skill/0.1").strip()
        area_cache_path = os.getenv("RAKUTEN_AREA_CACHE_PATH", "").strip() or None

        return cls(
            application_id=application_id,
            access_key=access_key,
            affiliate_id=affiliate_id,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            user_agent=user_agent,
            area_cache_path=area_cache_path,
        )

    def base_params(self) -> dict[str, str]:
        params = {
            "applicationId": self.application_id,
            "format": "json",
        }
        if self.access_key:
            params["accessKey"] = self.access_key
        if self.affiliate_id:
            params["affiliateId"] = self.affiliate_id
        return params

    def build_headers(self) -> dict[str, str]:
        headers = {"User-Agent": self.user_agent}
        if self.access_key:
            headers["Authorization"] = f"Bearer {self.access_key}"
        return headers


def _read_int(name: str, default: int, minimum: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer.") from exc
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}.")
    return value


def _read_float(name: str, default: float, minimum: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number.") from exc
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}.")
    return value

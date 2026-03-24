# OpenWeather Skill for OpenClaw

## Changelog

### 1.1.0 — Developer-plan-friendly API switch

- Replaced One Call 3.0 usage with `Current Weather API` and `5 day / 3 hour forecast API`.
- `current` no longer requires One Call by Call subscription.
- `forecast` now derives daily summaries from 3-hour forecast blocks and supports up to 5 days.
- `hourly` now uses 3-hour forecast steps and approximates the requested hour window.

### 1.0.1 — Documentation/behavior alignment

Fixes the previously noted doc vs. implementation mismatches:
- If no city is provided, the CLI now uses `OPENWEATHER_DEFAULT_LOCATION` (when set).
- Documentation no longer claims `curl` is used; the implementation uses Python `urllib` (stdlib).
- The “home location” mechanism is explicitly defined via `OPENWEATHER_DEFAULT_LOCATION` (env-based, no hidden config path).

### 1.0.2 — `.env` support

- The CLI now auto-loads `.env` from the skill root before reading environment variables.
- Existing shell environment variables still take precedence over `.env` values.

### 1.0.0 — Initial Public Release

## Why OpenWeather (and why this skill)

This skill uses OpenWeather endpoints that are commonly available to standard developer accounts:

- Current Weather API for live conditions
- 5 day / 3 hour forecast API for short-range forecast output

In practical terms:
- 1 API call per request
- Works without requiring One Call 3.0 subscription in the common case
- Stable, simple JSON payloads that are easy to relay in conversational output

## Subscription Requirement

This version avoids the One Call 3.0 dependency. It is intended to work with API keys that can access the standard Current Weather and 5 day / 3 hour Forecast endpoints.

## Forecast Products Supported

- Current weather (near real-time conditions)
- Short-range forecast via 3-hour forecast steps (up to 5 days)
- Daily forecast summaries derived from the 3-hour forecast feed

## Data Returned (high level)

- Conditions and descriptions
- Temperature and feels-like
- Humidity and pressure (where provided)
- Cloudiness and visibility (where provided)
- Wind speed/direction (where provided)
- Precipitation probability (PoP) in forecast responses
- Sunrise/sunset and timezone offsets in current weather responses

## Location Resolution

- City lookup is done directly via OpenWeather query parameters
- For ambiguous names, use “City, State, Country” or “City, Country”

## Conversational Output

- Human-readable CLI output intended for bots to relay

If you want Telegram-safe chunking and multi-message flows, that should be implemented at the agent layer (or add explicit chunking logic in a future version).

## Security and Configuration

- Config via environment variables, with optional auto-loading from a local `.env`
  - `OPENWEATHER_API_KEY` (required)
  - `OPENWEATHER_UNITS` (optional: imperial|metric|standard; default imperial)
  - `OPENWEATHER_DEFAULT_LOCATION` (optional default “home” location string)
- No hardcoded credentials
- No user data storage
- No external state required
- No elevated privileges required
- Network requests are restricted to OpenWeather domains only
- 1 API call per request

## Usage

Examples:

python3 scripts/weather.py current "New York, NY, US"
python3 scripts/weather.py forecast "Johnstown, PA, US" --days 5
python3 scripts/weather.py hourly "Johnstown, PA, US" --hours 12

Default home location:

export OPENWEATHER_DEFAULT_LOCATION="Johnstown, PA, US"
python3 scripts/weather.py current

Using `.env` in the skill root:

```dotenv
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_UNITS=metric
OPENWEATHER_DEFAULT_LOCATION=Tokyo, JP
```

Then run:

```bash
python3 scripts/weather.py current
python3 scripts/weather.py forecast --days 3
```

Environment variables already exported in your shell override values from `.env`.

Notes:

- `forecast --days` supports up to 5 days.
- `hourly --hours` uses OpenWeather's 3-hour forecast feed, so output is shown in 3-hour steps rather than true hourly intervals.

---
name: openweather
description: Get current weather, short-range hourly-style forecasts, and 5-day daily summaries for any location worldwide using OpenWeather standard APIs. Use when the user asks about weather, temperature, rain, snow, forecast, or conditions for any city or location.
metadata:
  openclaw:
    emoji: "🌤️"
    primaryEnv: OPENWEATHER_API_KEY
    requires:
      bins:
        - python3
      env:
        - OPENWEATHER_API_KEY
    config:
      env:
        OPENWEATHER_API_KEY:
          description: "Your OpenWeather API key for standard Current Weather / Forecast access."
          required: true
        OPENWEATHER_UNITS:
          description: "Units: imperial (°F), metric (°C), or standard (K)."
          default: "imperial"
          required: false
        OPENWEATHER_DEFAULT_LOCATION:
          description: "Optional default location used when no city is provided (example: Johnstown, PA, US)."
          required: false
---

# OpenWeather Skill

OpenWeather standard weather APIs via a small Python CLI (stdlib only).

The CLI auto-loads `.env` from the skill root if present. Exported environment variables still override `.env`.

## Commands

City is optional if `OPENWEATHER_DEFAULT_LOCATION` is set.

python3 {skillDir}/scripts/weather.py current [city]
python3 {skillDir}/scripts/weather.py forecast [city] --days 5
python3 {skillDir}/scripts/weather.py hourly [city] --hours 12

## Rules

- If no location is mentioned, use `OPENWEATHER_DEFAULT_LOCATION` when configured; otherwise ask the user for a location.
- Do not make more than 1 API call per request.
- `forecast` is based on OpenWeather's 5 day / 3 hour forecast and supports up to 5 days.
- `hourly` is a 3-hour-step forecast view, not a true 1-hour interval forecast.
- If the API returns 401, tell the user the key may be invalid or their OpenWeather plan may not include the requested endpoint.
- Do not claim to use curl; this skill uses Python urllib.

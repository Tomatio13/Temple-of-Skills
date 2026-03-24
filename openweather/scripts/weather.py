#!/usr/bin/env python3
"""
OpenWeather Current Weather + 5 Day / 3 Hour Forecast — CLI helper for OpenClaw

Usage:
  weather.py current [city] [--units imperial|metric|standard]
  weather.py forecast [city] [--days N] [--units imperial|metric|standard]
  weather.py hourly [city] [--hours N] [--units imperial|metric|standard]

If [city] is omitted, the script will use OPENWEATHER_DEFAULT_LOCATION (if set).
Example:
  OPENWEATHER_DEFAULT_LOCATION="Johnstown, PA, US" weather.py current
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_UNITS = {"imperial", "metric", "standard"}
DEFAULT_TIMEOUT_SECS = 12
USER_AGENT = "openclaw-openweather-skill/1.0 (+https://openweathermap.org/)"


def err(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_dotenv():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


load_dotenv()

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "").strip()
DEFAULT_LOCATION = os.environ.get("OPENWEATHER_DEFAULT_LOCATION", "").strip()


def fetch(url: str):
    # Only allow OpenWeather endpoints (HTTPS only).
    if not (url.startswith("https://api.openweathermap.org/") or url.startswith("https://openweathermap.org/")):
        err("Refusing to request non-OpenWeather URL")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT_SECS) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            msg = json.loads(body).get("message", body)
        except Exception:
            msg = body
        err(f"API error {e.code}: {msg}")
    except Exception as e:
        err(f"Request failed: {e}")


def current_weather(city, units):
    encoded = urllib.parse.quote(city)
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={encoded}&units={units}&appid={API_KEY}"
    )
    return fetch(url)


def forecast_3h(city, units, count=None):
    encoded = urllib.parse.quote(city)
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={encoded}&units={units}&appid={API_KEY}"
    )
    if count is not None:
        url += f"&cnt={count}"
    return fetch(url)


def wind_dir(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(deg / 45) % 8]


def fmt_time(ts, offset=0):
    dt = datetime.fromtimestamp(ts + offset, tz=timezone.utc)
    hour = int(dt.strftime("%I"))
    ampm = dt.strftime("%p")
    return dt.strftime(f"%a %b {dt.day}, {hour}:{dt.strftime('%M')} {ampm}")


def fmt_date(ts, offset=0):
    dt = datetime.fromtimestamp(ts + offset, tz=timezone.utc)
    return dt.strftime(f"%A, %b {dt.day}")


def local_date_key(ts, offset=0):
    dt = datetime.fromtimestamp(ts + offset, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")


def unit_labels(units):
    temp = {"imperial": "°F", "metric": "°C", "standard": "K"}.get(units, "°F")
    speed = {"imperial": "mph", "metric": "m/s", "standard": "m/s"}.get(units, "mph")
    return temp, speed


def summarize_day(entries):
    temps_min = [entry["main"]["temp_min"] for entry in entries]
    temps_max = [entry["main"]["temp_max"] for entry in entries]
    descriptions = [entry["weather"][0]["description"].title() for entry in entries]
    pops = [entry.get("pop", 0) for entry in entries]
    chosen_desc = Counter(descriptions).most_common(1)[0][0]
    return {
        "temp_min": min(temps_min),
        "temp_max": max(temps_max),
        "description": chosen_desc,
        "pop": max(pops),
    }


def cmd_current(city, units):
    temp_label, speed_label = unit_labels(units)
    data = current_weather(city, units)
    c = data
    offset = data.get("timezone", 0)
    resolved_name = data.get("name") or city
    sys_country = data.get("sys", {}).get("country", "")

    print(f"\n🌤️  Current Weather — {resolved_name}, {sys_country}")
    print(f"   As of: {fmt_time(c['dt'], offset)}")
    print(f"   {c['weather'][0]['description'].title()}")
    print(
        f"   Temperature: {c['main']['temp']:.0f}{temp_label}  "
        f"(feels like {c['main']['feels_like']:.0f}{temp_label})"
    )
    print(f"   Humidity: {c['main']['humidity']}%")
    print(f"   Wind: {c['wind']['speed']:.0f} {speed_label} {wind_dir(c['wind'].get('deg', 0))}")
    if "visibility" in c:
        vis = c["visibility"]
        print(f"   Visibility: {vis/1000:.0f} km" if units == "metric" else f"   Visibility: {vis/1609:.0f} mi")
    if "clouds" in c:
        print(f"   Cloudiness: {c['clouds'].get('all', 0)}%")
    if "sys" in c and c["sys"].get("sunrise") and c["sys"].get("sunset"):
        print(f"   Sunrise: {fmt_time(c['sys']['sunrise'], offset)}")
        print(f"   Sunset: {fmt_time(c['sys']['sunset'], offset)}")
    print()


def cmd_forecast(city, units, days=7):
    temp_label, _ = unit_labels(units)
    count = min(max(days, 1), 5) * 8
    data = forecast_3h(city, units, count=count)
    offset = data.get("city", {}).get("timezone", 0)
    resolved_name = data.get("city", {}).get("name") or city
    sys_country = data.get("city", {}).get("country", "")
    grouped = {}
    for entry in data.get("list", []):
        grouped.setdefault(local_date_key(entry["dt"], offset), []).append(entry)

    selected_days = list(grouped.values())[: min(max(days, 1), 5)]

    print(f"\n📅  {len(selected_days)}-Day Forecast — {resolved_name}, {sys_country}")
    print("   Based on OpenWeather 3-hour forecast data.\n")
    for entries in selected_days:
        summary = summarize_day(entries)
        date = fmt_date(entries[0]["dt"], offset)
        desc = summary["description"]
        hi = summary["temp_max"]
        lo = summary["temp_min"]
        pop = int(summary["pop"] * 100)
        rain_str = f"  💧{pop}% chance of rain" if pop >= 20 else ""
        print(f"  {date}")
        print(f"    {desc} — High {hi:.0f}{temp_label} / Low {lo:.0f}{temp_label}{rain_str}")
        print()


def cmd_hourly(city, units, hours=12):
    temp_label, _ = unit_labels(units)
    step_count = min(max((max(hours, 1) + 2) // 3, 1), 40)
    data = forecast_3h(city, units, count=step_count)
    offset = data.get("city", {}).get("timezone", 0)
    resolved_name = data.get("city", {}).get("name") or city
    sys_country = data.get("city", {}).get("country", "")
    hourly = data.get("list", [])[:step_count]

    print(f"\n⏰  Next ~{min(max(hours, 1), 120)} Hours — {resolved_name}, {sys_country}")
    print("   3-hour step forecast from OpenWeather.\n")
    for h in hourly:
        time = fmt_time(h["dt"], offset)
        temp = h["main"]["temp"]
        desc = h["weather"][0]["description"].title()
        pop = int(h.get("pop", 0) * 100)
        rain_str = f"  💧{pop}%" if pop >= 20 else ""
        print(f"  {time:<26}  {temp:.0f}{temp_label}  {desc}{rain_str}")
    print()


def parse_args():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    city_parts = []
    flags = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--"):
            if i + 1 < len(args):
                flags[args[i]] = args[i + 1]
                i += 2
            else:
                i += 1
        else:
            city_parts.append(args[i])
            i += 1

    city = " ".join(city_parts).strip() if city_parts else ""
    if not city:
        if DEFAULT_LOCATION:
            city = DEFAULT_LOCATION
        else:
            err(
                "No city provided and OPENWEATHER_DEFAULT_LOCATION is not set.\n"
                "Examples:\n"
                '  weather.py current "New York, NY, US"\n'
                '  export OPENWEATHER_DEFAULT_LOCATION="Johnstown, PA, US"'
            )

    units = flags.get("--units", os.environ.get("OPENWEATHER_UNITS", "imperial")).strip().lower()
    if units not in ALLOWED_UNITS:
        err(f"Invalid units: '{units}'. Use: imperial, metric, or standard")

    days = int(flags.get("--days", 7))
    hours = int(flags.get("--hours", 12))
    return cmd, city, units, days, hours


def main():
    if not API_KEY:
        err(
            "OPENWEATHER_API_KEY is not set.\n"
            "Get a key at https://openweathermap.org/api\n"
            "Then set it in your OpenClaw skill config or as an environment variable."
        )

    cmd, city, units, days, hours = parse_args()

    if cmd == "current":
        cmd_current(city, units)
    elif cmd == "forecast":
        cmd_forecast(city, units, days)
    elif cmd == "hourly":
        cmd_hourly(city, units, hours)
    else:
        err(f"Unknown command: '{cmd}'. Valid commands: current, forecast, hourly")


if __name__ == "__main__":
    main()

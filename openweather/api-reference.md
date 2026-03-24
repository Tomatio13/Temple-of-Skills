# OpenWeather Current Weather + 5 Day / 3 Hour Forecast — Quick Reference

## Endpoints

### Current Weather
```
GET https://api.openweathermap.org/data/2.5/weather
  ?q={city name},{state code},{country code}
  &units={imperial|metric|standard}
  &appid={API_KEY}
```

### 5 day / 3 hour forecast
```
GET https://api.openweathermap.org/data/2.5/forecast
  ?q={city name},{state code},{country code}
  &units={imperial|metric|standard}
  &appid={API_KEY}
```

## Response Fields (current)
| Field | Description |
|-------|-------------|
| `dt` | Unix timestamp |
| `temp` | Temperature |
| `feels_like` | Perceived temperature |
| `humidity` | % humidity |
| `wind_speed` | Wind speed |
| `wind_deg` | Wind direction (degrees) |
| `visibility` | Visibility in metres |
| `weather[0].description` | Condition text |

## Response Fields (forecast item)
| Field | Description |
|-------|-------------|
| `dt` | Unix timestamp |
| `main.temp` | Forecast temperature |
| `main.temp_min` / `main.temp_max` | Temperature range for the block |
| `pop` | Probability of precipitation (0–1) |
| `weather[0].description` | Condition text |

## Rate Limits
- Free tier: 1,000 calls/day
- Paid: pay-per-call beyond free tier
- Endpoint availability depends on your OpenWeather plan

## Error Codes
| Code | Meaning |
|------|---------|
| 401 | Invalid API key or plan does not include the endpoint |
| 404 | Location not found |
| 429 | Rate limit exceeded |
| 5xx | Server error — retry |

# Weather Anomaly Detection — Backend API

Backend service for the SIH Weather Station Anomaly Detection project. Serves historical weather data (from Meteostat) over HTTP, with filtering support, for consumption by the dashboard frontend.

## Tech Stack

- **FastAPI** — web framework for defining and serving HTTP endpoints
- **Uvicorn** — ASGI server that actually runs the FastAPI app
- **Pandas** — loads and filters the weather dataset in memory

## Running the server

```bash
# Activate the virtual environment first
.\venv\Scripts\Activate.ps1        # Windows PowerShell

# Start the server (auto-reloads on code changes)
uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

Interactive API docs (auto-generated, testable in-browser): `http://127.0.0.1:8000/docs`

## Data

- **Source file:** `india_weather_2025_january.csv` (configurable via the `CSV_FILE` constant at the top of `main.py`)
- Loaded once into memory when the server starts (not re-read per request)
- Exact duplicate rows are automatically removed on load
- Missing/empty values (e.g. `snwd`, `wpgt`, `tsun` for stations that don't report them) are serialized as JSON `null`

### Columns

| Column | Meaning |
|---|---|
| `time` | Timestamp of the reading (ISO format in API responses) |
| `temp` | Air temperature (°C) |
| `rhum` | Relative humidity (%) |
| `prcp` | Precipitation (mm) |
| `snwd` | Snow depth (mm) — usually `null` for Indian stations |
| `wdir` | Wind direction (degrees) |
| `wspd` | Wind speed (km/h) |
| `wpgt` | Wind gust (km/h) — often `null` |
| `pres` | Sea-level air pressure (hPa) |
| `tsun` | Sunshine duration (minutes) — often `null` |
| `cldc` | Cloud cover code |
| `coco` | Weather condition code (Meteostat code) |
| `station_id` | Unique numeric station identifier |
| `station_name` | Human-readable station name |

## Endpoints

### `GET /`

Health check.

**Response:**
```json
{ "message": "Weather anomaly backend is running" }
```

---

### `GET /weather`

Returns weather readings. All query parameters are optional and can be combined.

| Parameter | Type | Example | Description |
|---|---|---|---|
| `station_id` | integer | `42137` | Filter to a single station by ID |
| `station_name` | string | `Karnal` | Filter to a single station by name |
| `start` | string (`YYYY-MM-DD`) | `2025-01-10` | Only include readings from this date onward |
| `end` | string (`YYYY-MM-DD`) | `2025-01-15` | Only include readings up to and including this date |

**Examples:**
```
GET /weather
GET /weather?station_id=42137
GET /weather?station_name=Meerut
GET /weather?start=2025-01-05&end=2025-01-07
GET /weather?station_id=42137&start=2025-01-05&end=2025-01-07
```

**Response:** JSON array of weather reading objects, e.g.
```json
[
  {
    "time": "2025-01-01T00:00:00.000",
    "temp": 7.2,
    "rhum": 100,
    "prcp": 0.0,
    "snwd": null,
    "wdir": 304,
    "wspd": 11.5,
    "wpgt": null,
    "pres": 1018.9,
    "tsun": null,
    "cldc": 8,
    "coco": 5,
    "station_id": 42137,
    "station_name": "Karnal"
  }
]
```

**Errors:**
- `400 Bad Request` — if `start` or `end` is not a valid date in `YYYY-MM-DD` format
- `422 Unprocessable Entity` — if `station_id` is not a valid integer (handled automatically by FastAPI)
- A station/date filter that matches no rows returns an empty array `[]`, not an error

---

### `GET /stations`

Returns the list of unique stations available in the dataset. Useful for populating a dropdown/filter list in the frontend without pulling the full weather dataset.

**Response:**
```json
[
  { "station_id": 42137, "station_name": "Karnal" },
  { "station_id": 42139, "station_name": "Meerut" },
  { "station_id": 42176, "station_name": "Rohtak" },
  { "station_id": 42181, "station_name": "Palam" },
  { "station_id": 42182, "station_name": "Safdarjung" },
  { "station_id": 42262, "station_name": "Aligarh" }
]
```

---

## CORS

CORS is enabled for all origins (`allow_origins=["*"]`), so the API can be called directly from frontend JavaScript running on any domain/port during development. This should be restricted to the actual frontend's domain before any production deployment.

## Known limitations / not yet implemented

- **Anomaly detection results** (`/anomalies` or similar) are not yet exposed — pending integration with the Isolation Forest model output from the ML teammate.
- Data is loaded once at server startup; if the underlying CSV changes, the server needs to be restarted to pick up new data (no live reload of the dataset itself).
- No authentication/rate limiting — not needed for the current prototype scope.

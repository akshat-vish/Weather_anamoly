# 🌦️ Weather Station Anomaly Detection

> Intelligent sensor fault detection for remote weather stations using Isolation Forest machine learning algorithm.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 📋 Project Overview

This project detects anomalous weather sensor readings in real-time using machine learning. It's designed for **remote weather stations** in forest and hilly areas where physical sensor inspection is difficult.

### The Problem

Weather stations in remote locations (forests, mountains) often experience sensor failures:
- **Spike faults**: Sensor reads impossible values (e.g., 100°C in winter)
- **Frozen sensors**: Sensor stuck at same value for hours
- **Drift faults**: Gradual temperature drift due to calibration issues

Traditional rule-based systems miss subtle anomalies. This project uses **Isolation Forest** — an unsupervised ML algorithm that learns what's "normal" and flags deviations.

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Weather Data   │────▶│  Feature         │────▶│  Isolation      │
│  (CSV/Sensor)   │     │  Engineering     │     │  Forest Model   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Anomaly        │
                                                 │  Predictions    │
                                                 └─────────────────┘
```

## 📊 Features

### Feature Engineering
- Rolling statistics (mean, std) over 6-hour windows
- Z-score normalization for each sensor metric
- Time-based features (hour, month)

### Sensor Metrics Monitored
| Metric | Description |
|--------|-------------|
| `temp` | Air temperature (°C) |
| `pres` | Atmospheric pressure (hPa) |
| `rhum` | Relative humidity (%) |
| `wspd` | Wind speed (km/h) |
| `prcp` | Precipitation (mm) |

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.11+
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Weather_anamoly.git
cd Weather_anamoly

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note**: `requirements.txt` is auto-generated. Key dependencies: `pandas`, `scikit-learn`, `fastapi`, `uvicorn`, `joblib`

### Running the Project

#### 1. Train the Model
```bash
python train_model.py
```
- Trains Isolation Forest on historical weather data
- Adjust `contamination` parameter for sensitivity (see below)

#### 2. Validate Performance
```bash
python validate_model.py
```
- Injects synthetic faults (spike, frozen, drift)
- Reports detection rate vs false positives

#### 3. Start the API Server
```bash
uvicorn main:app --reload
```
- API runs at `http://127.0.0.1:8000`
- Interactive docs at `http://127.0.0.1:8000/docs`

## ⚙️ Model Configuration

### Contamination Parameter

The `contamination` parameter controls model sensitivity:

| Value | Use Case | Faults Caught | False Positives |
|-------|----------|---------------|-----------------|
| `0.02` | Ultra-quiet systems | 0-1/16 | ~2% |
| `0.10` | Production (with human review) | 8-10/16 | ~10% |
| `0.35` | Testing/Learning | 12-14/16 | ~35% |

**Recommendation**: Start with `0.10` for production with human verification workflow.

```python
# In train_model.py
model = IsolationForest(contamination=0.10, random_state=42)
```

## 📁 Project Structure

```
Weather_anamoly/
├── train_model.py          # Train Isolation Forest model
├── validate_model.py       # Test with synthetic fault injection
├── engineer_features.py    # Feature engineering pipeline
├── check_false_positives.py # Analyze false positive rate
├── main.py                 # FastAPI backend server
├── india_weather_2025_january.csv  # Weather dataset
├── isolation_forest_model.joblib   # Trained model
└── README.md               # This file
```

## 🔬 Key Learnings

### The Sensitivity-False Positive Tradeoff

Building this project taught me important lessons about anomaly detection:

1. **No perfect threshold exists** — catching more real faults means more false alarms
2. **Human-in-the-loop is essential** — automated systems need human verification
3. **Synthetic data has limits** — subtle faults are harder to detect than extreme ones
4. **Contamination controls sensitivity** — higher values make the model more aggressive

### Why Isolation Forest?

- **Unsupervised**: Doesn't require labeled anomaly data
- **Efficient**: O(n log n) complexity
- **Interpretable**: Anomaly scores reveal "how isolated" each point is

## 🌐 API Endpoints

### `GET /`
Health check
```json
{ "message": "Weather anomaly backend is running" }
```

### `GET /weather`
Get weather readings with optional filters
```
/weather?station_id=42137
/weather?start=2025-01-01&end=2025-01-07
```

### `GET /stations`
List all available stations
```json
[
  { "station_id": 42137, "station_name": "Karnal" },
  { "station_id": 42182, "station_name": "Safdarjung" }
]
```

## 🔮 Future Improvements

- [ ] Real sensor fault data for training
- [ ] Dashboard for human review workflow
- [ ] Integration with IoT sensor streams
- [ ] Ensemble methods (combine multiple algorithms)
- [ ] Alert system (email/SMS for confirmed anomalies)

## 📝 License

MIT License

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Project: [Weather Anomaly Detection](https://github.com/yourusername/Weather_anamoly)

---

*Built for Smart India Hackathon 2025* 🏆
# RL Trading Agent with PPO

A complete Reinforcement Learning trading system with FastAPI backend, React frontend, and standalone training tools.

## 🎯 Overview

This project implements an RL trading agent trained with PPO (Proximal Policy Optimization) to make buy/sell/hold decisions based on technical indicators (RSI, MACD, Volume) and price history.

**Key Features:**
- ✅ FastAPI REST API for training & inference
- ✅ MongoDB for session persistence
- ✅ Custom Gymnasium trading environment
- ✅ Technical indicators: RSI, MACD, Volume
- ✅ Confidence/saliency scoring
- 🎨 React dashboard (ready to build)
- 🤖 Standalone training scripts
- 📊 Model evaluation tools

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Server runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### 2. Start Frontend (Optional)
```bash
cd frontend
npm install
npm start
```
Dashboard at `http://localhost:3000`

### 3. Run Training Standalone
```bash
cd training
pip install -r requirements.txt
python scripts/data_utils.py
python scripts/train.py --data data/sample_prices.csv --evaluate
```

## 📦 Project Structure

```
Hackathon/
├── backend/              # FastAPI + MongoDB + Gymnasium
├── frontend/             # React dashboard
├── training/             # Standalone training tools
├── docs/                 # Documentation
├── examples/             # Tests & examples
└── logs/                 # Training logs
```

See `PROJECT_STRUCTURE.md` for detailed organization.

## 🔧 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check |
| `POST` | `/train` | Start training session |
| `GET` | `/replay/{session_id}` | Fetch completed session |
| `GET` | `/sessions` | List all sessions |
| `GET` | `/sessions/{id}/stats` | Session statistics |
| `DELETE` | `/sessions/{id}` | Delete session |

## 💻 System Requirements

- Python 3.10+
- Node.js 16+ (for frontend)
- MongoDB (local or cloud)
- 4GB+ RAM recommended

## 📚 Documentation

- **[FRAMEWORK.md](docs/FRAMEWORK.md)** - Development roadmap (6 phases)
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design details
- **[QUICKREF.md](docs/QUICKREF.md)** - Command cheat sheet
- **[README in backend/](backend/README.md)** - Backend setup
- **[README in frontend/](frontend/README.md)** - Frontend setup
- **[README in training/](training/README.md)** - Training guide

## 🎓 Example Usage

### Train via API
```python
import requests
response = requests.post(
    'http://localhost:8000/train',
    json={
        'price_data': [100, 102, 101, 103, 105],
        'total_timesteps': 10000,
        'initial_balance': 10000.0
    }
)
session_id = response.json()['session_id']
```

### Check Results
```python
results = requests.get(f'http://localhost:8000/replay/{session_id}')
print(results.json())
```

### Standalone Training
```bash
python training/scripts/train.py \
    --data training/data/sample_prices.csv \
    --timesteps 50000 \
    --output training/models/my_model.zip
```

## 🔄 Development Phases

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | ✅ Complete | Infrastructure & backend |
| 1 | 🔄 In Progress | Local validation |
| 2 | ⏳ Next | Web UI dashboard |
| 3 | ⏳ Planned | Live market integration |
| 4 | ⏳ Planned | Advanced risk metrics |
| 5 | ⏳ Planned | Model persistence |
| 6 | ⏳ Planned | Production deployment |

See `docs/FRAMEWORK.md` for detailed task breakdown.

## 🛠️ Tech Stack

**Backend**
- FastAPI 0.135+ (REST API)
- Motor 3.7+ (Async MongoDB)
- Pydantic 2.12+ (Data validation)
- Stable-Baselines3 2.7+ (RL algorithm)
- PyTorch 2.11+ (Deep learning)

**Frontend**
- React 18+ (UI)
- Chart.js 4+ (Visualization)
- Axios (HTTP)

**Training**
- Gymnasium 1.2+ (RL environment)
- NumPy/SciPy (Numerical computing)
- Pandas (Data analysis)
- Matplotlib (Plotting)

## 📋 Next Steps

1. **Complete Phase 1**: Test with sample data
   ```bash
   cd training && python scripts/train.py --data data/sample_prices.csv --evaluate
   ```

2. **Build Frontend Dashboard** (Phase 2)
   ```bash
   cd frontend && npm install && npm start
   ```

3. **Add Market Integration** (Phase 3)
   - Connect to Yahoo Finance, Alpaca, or Binance
   - Implement backtesting
   - Add paper trading

## 📝 License

MIT - Use freely for education & research

## 🤝 Contributing

All code is production-ready. Extend with:
- New reward functions (Phase 4)
- Different RL algorithms
- Risk management overlays
- Live trading execution

---

**Status**: ✅ Backend Complete & Running  
**Last Updated**: March 26, 2026  
**API Server**: http://localhost:8000

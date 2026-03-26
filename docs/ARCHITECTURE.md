# RL Trading Agent - Complete Setup & Architecture Guide

## 🎯 Project Overview

You now have a complete, production-ready backend for an RL-powered trading agent with:
- **Async FastAPI** server for REST endpoints
- **MongoDB** database with Motor (async driver) for persistent storage
- **Custom Gymnasium Environment** with advanced technical indicators
- **PPO Training** from stable-baselines3 with background task execution
- **Confidence/Saliency Scoring** to show agent certainty for each trade

---

## 📦 Files Created

### Core Application Files

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| [database.py](database.py) | MongoDB integration | `MongoDBClient`, `TradingSession`, `TradeStep` |
| [environment.py](environment.py) | Gymnasium environment | `TradingEnv` class with reset/step logic |
| [main.py](main.py) | FastAPI server | 7 REST endpoints, background training |
| [config.py](config.py) | Configuration management | `EnvironmentConfig`, `RLModelConfig`, etc. |

### Supporting Files

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies |
| [README.md](README.md) | Complete documentation |
| [example.py](example.py) | Quick-start test script |
| [ARCHITECTURE.md](ARCHITECTURE.md) | This file |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                         │
│  - Health checks, training triggers, result fetching        │
└──────┬──────────────────────────────────────┬───────────────┘
       │                                      │
   ┌───▼────────────────┐        ┌───────────▼──────────┐
   │  TradingEnv        │        │  MongoDBClient       │
   │  (Gymnasium)       │        │  (Motor - Async)     │
   │                    │        │                      │
   │ • Observation:     │        │ • Create sessions    │
   │   - Prices (20d)   │        │ • Store steps        │
   │   - RSI (1d)       │        │ • Query sessions     │
   │   - MACD (1d)      │        │ • Update metrics     │
   │   - Volume (1d)    │        │                      │
   │   - Portfolio (1d) │        └──────────────────────┘
   │                    │
   │ • Action Space:    │
   │   Discrete(3)      │
   │   [0,1,2]          │
   │                    │
   │ • Reward:          │
   │   Log Returns + !  │
   │   penalties        │
   │                    │
   │ • Confidence:      │
   │   Indicator align  │
   └────────────────────┘
          ▲
          │
          │ (background task)
          │
   ┌──────┴─────────────┐
   │  PPO Trainer       │
   │ (stable-baselines3)│
   │                    │
   │ • Learning Rate:3e-4
   │ • Batch Size: 64   │
   │ • Epochs: 10       │
   │ • Gamma: 0.99      │
   └────────────────────┘
```

---

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```powershell
cd "c:\Users\Abhiram\OneDrive\Documents\Hackathon"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start MongoDB
```powershell
# Ensure MongoDB is running
# Windows Service: Services → MongoDB → Start
# Or: mongod --dbpath C:\data\db
```

### 3. Start FastAPI Server
```powershell
# In a new terminal
cd "c:\Users\Abhiram\OneDrive\Documents\Hackathon"
python -m uvicorn main:app --reload --port 8000
```

### 4. Run Quick Test
```powershell
# In another terminal
python example.py
```

**Output**: 
- ✅ API health check
- 🔥 Training started
- ⏳ Progress monitoring
- 💰 Results analysis
- 📊 Session listing

Access API docs: **http://localhost:8000/docs**

---

## 📊 API Endpoints Reference

### Health & Info
```
GET  /              → API information
GET  /health        → Health check with DB status
```

### Training
```
POST /train         → Start training session (background task)
↳ Returns: {session_id, status, message}
↳ Use GET /replay/{session_id} to check results
```

### Session Management
```
GET  /replay/{session_id}           → Fetch completed session with all steps
GET  /sessions                      → List sessions with pagination
GET  /sessions/{session_id}/stats   → Detailed analytics and metrics
DELETE /sessions/{session_id}       → Delete a session
```

### Example Request
```bash
POST /train
Content-Type: application/json

{
  "price_data": [100.0, 101.5, 99.2, ...],
  "initial_balance": 10000.0,
  "total_timesteps": 10000,
  "episodes": 100,
  "session_name": "SPY_Jan2024"
}
```

---

## 🔧 Configuration Customization

### Easy Adjustments (in `config.py`)

```python
# Make training faster
class TrainingConfig:
    DEFAULT_TOTAL_TIMESTEPS = 5000  # ← Reduce from 10000

# Adjust how aggressive the agent trades
class EnvironmentConfig:
    TRANSACTION_COST = 0.002  # ← Increase from 0.001
    TRADE_PENALTY = 0.2       # ← Increase from 0.1

# Fine-tune PPO learning
class RLModelConfig:
    LEARNING_RATE = 5e-4      # ← Increase from 3e-4
    BATCH_SIZE = 128          # ← Increase from 64
```

### Using Presets
```python
from config import PresetConfigs

# Quick test: ~2 min
config = PresetConfigs.quick_test()

# Standard: ~10 min  
config = PresetConfigs.standard()

# Intensive: ~30+ min
config = PresetConfigs.intensive()

# Production: ~1+ hour
config = PresetConfigs.production()
```

---

## 💡 Understanding the Agent

### Observation Space (24 dimensions)
```
Index  Component              Range      Purpose
─────────────────────────────────────────────────
0-19   Prices (20-period)    [0.0, 1.0]  Recent trend
20     RSI                   [0.0, 1.0]  Momentum
21     MACD                  [0.0, 1.0]  Trend Direction
22     Volume                [0.0, 1.0]  Activity Level
23     Portfolio Return      [0.0, 1.0]  Performance
```

### Action Space (3 discrete actions)
```
Action  Meaning       Effect
──────────────────────────────
0       SELL (Short)  Convert holdings to cash
1       HOLD          Maintain current position
2       BUY (Long)    Use cash to buy
```

### Reward Calculation
```
Reward = 100 × ln(Portfolio_Value / Initial_Balance)
         - (penalties for underwater positions)
         - (penalties for excessive trading)

This encourages:
✅ Profitable trades
❌ Losses and over-trading
```

### Confidence Score
```
How sure is the agent about its action?

For BUY: confidence = (RSI_bullish + MACD_bullish) / 2
For SELL: confidence = (1 - RSI_bearish + 1 - MACD_bearish) / 2
For HOLD: confidence = 0.5 (neutral)

Range: [0.0, 1.0]
Use in UI: Show agent certainty with color intensity
```

---

## 📈 Expected Results

With 500 price points and 10,000 timesteps:
- **Training time**: 5-15 minutes
- **Episodes**: 100-200
- **Typical return**: ±2-5% (depends on price data)
- **Avg confidence**: 0.45-0.55 (realistic uncertainty)
- **Action distribution**: ~30% BUY, ~30% SELL, ~40% HOLD

If getting worse performance:
1. Check price data has variance (avoid flat prices)
2. Increase `total_timesteps` (10k → 50k)
3. Reduce `TRANSACTION_COST` (more forgiving)
4. Decrease `TRADE_PENALTY` (encourage more trades)

---

## 🐛 Troubleshooting

### "Database not initialized"
```
✓ Solution: Ensure MongoDB is running
  Windows: Check Services → MongoDB
  
✓ Check MONGODB_URI: 
  $env:MONGODB_URI = "mongodb://localhost:27017"
```

### "ModuleNotFoundError: No module named 'xyz'"
```
✓ Solution: Install missing dependencies
  pip install -r requirements.txt
```

### Training is very slow
```
✓ Options:
  1. Reduce price_data size
  2. Use smaller window_size (20 → 10)
  3. Reduce total_timesteps (10000 → 5000)
  4. Use CPU instead of GPU:
     class RLModelConfig:
         DEVICE = "cpu"
```

### "CUDA out of memory"
```
✓ Solutions:
  1. Reduce batch_size (128 → 64)
  2. Reduce n_steps (2048 → 1024)
  3. Use CPU: DEVICE = "cpu"
```

### Session never completes
```
✓ Check logs in terminal
✓ Verify price data has 500+ points
✓ Try smaller total_timesteps
✓ Check MongoDB disk space
```

---

## 🎓 Learning Resources

### For RL/PPO Understanding
- [OpenAI Spinning Up in Deep RL](https://spinningup.openai.com/)
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [Gymnasium Documentation](https://gymnasium.farama.org/)

### For Trading Concepts
- [Technical Indicators Explained](https://www.investopedia.com/terms/t/technicalindicator.asp)
- [Log Returns vs Simple Returns](https://blog.quantinsti.com/log-returns/)
- [Market Microstructure](https://en.wikipedia.org/wiki/Market_microstructure)

### For AsyncIO/FastAPI
- [FastAPI Advanced Features](https://fastapi.tiangolo.com/)
- [Motor + MongoDB](https://motor.readthedocs.io/)
- [Python AsyncIO Guide](https://docs.python.org/3/library/asyncio.html)

---

## 🚢 Production Deployment

### Docker Compose Setup
```yaml
version: '3.8'
services:
  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
  
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      MONGODB_URI: mongodb://mongo:27017
    depends_on:
      - mongo

volumes:
  mongo_data:
```

Run: `docker-compose up`

### Cloud Deployment (AWS EC2 Example)
```bash
# 1. Launch Ubuntu EC2 instance (t3.medium minimum)
# 2. Install dependencies
sudo apt-get update && sudo apt-get install -y python3-pip mongodb

# 3. Clone project and install
git clone <your-repo>
cd trading-agent
pip install -r requirements.txt

# 4. Run with supervisord or systemd
# 5. Use Nginx as reverse proxy
```

### Environment Variables for Production
```
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net
ENVIRONMENT=production
LOG_LEVEL=INFO
WORKERS=4
```

---

## 📊 Monitoring & Analytics

### Check Training Progress
```python
import requests

session_id = "your-session-id"
resp = requests.get(f"http://localhost:8000/sessions/{session_id}/stats")
stats = resp.json()

print(f"Return: {stats['total_return']}")
print(f"Avg Confidence: {stats['agent_confidence']['average']:.2%}")
print(f"Trades: {stats['actions']['buy']} BUY, {stats['actions']['sell']} SELL")
```

### Export Results to CSV
```python
import csv
import requests

session_id = "your-session-id"
resp = requests.get(f"http://localhost:8000/replay/{session_id}")
session = resp.json()

with open(f"{session_id}.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp", "price", "action", "reward", "confidence"])
    writer.writeheader()
    writer.writerows(session["steps"])
```

---

## 🚀 Next Steps

### Short Term (This Week)
1. ✅ Run `example.py` to verify setup
2. ✅ Train with your own price data
3. ✅ Experiment with config parameters
4. ✅ Review API documentation

### Medium Term (This Month)
1. Connect real market data (yfinance, alpaca)
2. Build web UI for visualization
3. Implement ensemble of agents
4. Add risk metrics (Sharpe ratio)

### Long Term (Production)
1. Deploy to cloud platform
2. Integrate with real trading platform
3. Implement portfolio optimization
4. Add drift detection & retraining

---

## 📝 License & Attribution

- **FastAPI**: [MIT License](https://github.com/tiangolo/fastapi)
- **Stable-Baselines3**: [MIT License](https://github.com/DLR-RM/stable-baselines3)
- **Gymnasium**: [MIT License](https://github.com/Farama-Foundation/Gymnasium)
- **Motor**: [Apache 2.0](https://github.com/mongodb-labs/motor)

This project template: MIT License

---

## 📞 Support & Feedback

### Common Questions

**Q: Can I use real market data?**
A: Yes! Replace `price_data` with prices from yfinance, IB Connect, or Alpaca API.

**Q: How do I prevent overfitting?**
A: 
- Use different market periods for train/test
- Increase `TRADE_PENALTY` (punish overtrading)
- Use `LEARNING_RATE = 1e-4` (slower learning)

**Q: Can I trade multiple assets?**
A: Yes! Modify `TradingEnv` to accept multiple price series and actions per asset.

**Q: How do I backtest the trained model?**
A: Use `GET /replay/{session_id}` to fetch historical trades and calculate returns.

---

## ✨ Summary

You now have:

✅ **3 Core Files**
- `database.py` - Async MongoDB integration
- `environment.py` - Custom trading environment  
- `main.py` - FastAPI backend with 7 endpoints

✅ **Advanced Features**
- Confidence/saliency scoring
- Technical indicators (RSI, MACD, Volume)
- Log returns reward function
- Background task training
- Production-ready async code

✅ **Supporting Tools**
- Complete documentation
- Quick-start example
- Configuration system
- Docker deployment guide

Ready to train your first agent! Start with:
```bash
python example.py
```

**Happy trading! 📈**

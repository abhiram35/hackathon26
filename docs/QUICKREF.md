# RL Trading Agent - Quick Reference Guide

## 🚀 Getting Started

### First Setup
```powershell
# 1. Navigate to project
cd "c:\Users\Abhiram\OneDrive\Documents\Hackathon"

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start MongoDB (ensure it's running)
# Windows: Services → MongoDB → Start
# Or: mongod --dbpath C:\data\db
```

### Every Session
```powershell
# Activate venv
venv\Scripts\activate

# Start API server
python -m uvicorn main:app --reload --port 8000

# In another terminal, run tests
python example.py
```

---

## 📡 API Endpoints Cheat Sheet

### Health Check
```bash
# Test if API is running
curl http://localhost:8000/health

# Expected: {"status": "healthy", "database": "✓ Connected", ...}
```

### Start Training
```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "price_data": [100, 101.5, 99.2, ...],
    "initial_balance": 10000,
    "total_timesteps": 5000,
    "episodes": 50
  }'

# Returns: {"session_id": "abc-123...", "status": "queued"}
```

### Fetch Results
```bash
# Replace session_id with actual ID
curl http://localhost:8000/replay/abc-123-def-456

# Returns: Complete session with all steps and metrics
```

### List Sessions
```bash
curl "http://localhost:8000/sessions?limit=10"

# Returns: List of all sessions with stats
```

### Session Statistics
```bash
curl http://localhost:8000/sessions/abc-123-def-456/stats

# Returns: Detailed metrics (confidence, trades, returns)
```

### Delete Session
```bash
curl -X DELETE http://localhost:8000/sessions/abc-123-def-456

# Returns: {"message": "Session deleted successfully"}
```

---

## 🐍 Python Usage Examples

### Test Connectivity
```python
import requests

# Health check
resp = requests.get("http://localhost:8000/health")
print(resp.json())
```

### Generate & Train
```python
import requests
import numpy as np

# Synthetic prices
prices = (100 + np.cumsum(np.random.randn(500) * 2)).tolist()

# Submit training
resp = requests.post("http://localhost:8000/train", json={
    "price_data": prices,
    "initial_balance": 10000,
    "total_timesteps": 10000
})

session_id = resp.json()["session_id"]
print(f"Training session: {session_id}")
```

### Monitor Training
```python
import requests
import time

session_id = "your-session-id"

while True:
    resp = requests.get(f"http://localhost:8000/replay/{session_id}")
    data = resp.json()
    
    print(f"Status: {data['status']}")
    
    if data["status"] == "completed":
        print(f"Return: {data['total_return']*100:+.2f}%")
        break
    
    time.sleep(10)
```

### Analyze Results
```python
import requests
import numpy as np

session_id = "your-session-id"
resp = requests.get(f"http://localhost:8000/replay/{session_id}")
session = resp.json()

steps = session["steps"]
confidences = [s["agent_confidence"] for s in steps]
actions = [s["action"] for s in steps]

print(f"Avg Confidence: {np.mean(confidences):.2%}")
print(f"Max Confidence: {np.max(confidences):.2%}")
print(f"Buy Count: {sum(1 for a in actions if a == 2)}")
print(f"Sell Count: {sum(1 for a in actions if a == 0)}")
```

---

## 🔧 Configuration Quick Changes

### Make Training Faster
```python
# config.py - Change:
class TrainingConfig:
    DEFAULT_TOTAL_TIMESTEPS: int = 5000  # ← from 10000

class EnvironmentConfig:
    WINDOW_SIZE: int = 10  # ← from 20
```

### Make Agent More Conservative
```python
# config.py - Change:
class EnvironmentConfig:
    TRADE_PENALTY: float = 0.2  # ← from 0.1
    TRANSACTION_COST: float = 0.002  # ← from 0.001
```

### More Aggressive Learning
```python
# config.py - Change:
class RLModelConfig:
    LEARNING_RATE: float = 5e-4  # ← from 3e-4
    CLIP_RANGE: float = 0.3  # ← from 0.2
```

---

## 📊 File Structure

```
Hackathon/
├── main.py                 ← FastAPI app (7 endpoints)
├── database.py             ← MongoDB async driver + schemas
├── environment.py          ← Custom Gymnasium environment
├── config.py               ← Configuration management
├── requirements.txt        ← Python dependencies
├── example.py              ← Quick-start test script
├── README.md               ← Full documentation
├── ARCHITECTURE.md         ← Detailed architecture guide
└── QUICKREF.md            ← This file
```

---

## 🐛 Common Issues & Fixes

### "Connection refused: MongoDB"
```
✓ Fix: Start MongoDB
  mongod --dbpath C:\data\db
  
✓ Verify: curl mongodb://localhost:27017
```

### "Module not found: gymnasium"
```
✓ Fix: Install dependencies
  pip install -r requirements.txt
  
✓ Verify: python -c "import gymnasium; print(gymnasium.__version__)"
```

### "Training stuck / not progressing"
```
✓ Check: 
  - MongoDB has free space
  - Price data isn't flat/constant
  - total_timesteps > 1000
  
✓ Fix:
  - Reduce WINDOW_SIZE from 20 → 10
  - Increase LEARNING_RATE from 3e-4 → 5e-4
  - Reduce BATCH_SIZE from 64 → 32
```

### "API returns 404 (not found)"
```
✓ Check:
  - Session ID is correct
  - Training is actually completed
  
✓ Test: GET /sessions (list all)
```

---

## 📈 Performance Tuning

### For Faster Training
```python
# Reduce processing
WINDOW_SIZE = 10  # 20 → 10
BATCH_SIZE = 32   # 64 → 32
N_STEPS = 1024    # 2048 → 1024

# Shorter episodes
DEFAULT_TOTAL_TIMESTEPS = 2000  # 10000 → 2000
```

### For Better Results  
```python
# Longer training
DEFAULT_TOTAL_TIMESTEPS = 50000  # 10000 → 50000
N_EPOCHS = 20  # 10 → 20
LEARNING_RATE = 1e-4  # 3e-4 → 1e-4

# Larger batch
BATCH_SIZE = 128  # 64 → 128
```

### For Production Use
```python
# Robust training
DEFAULT_TOTAL_TIMESTEPS = 100000
BATCH_SIZE = 256
LEARNING_RATE = 1e-4
N_EPOCHS = 20
CLIP_RANGE = 0.15  # More conservative
```

---

## 🎯 Key Equations

### Reward (Log Returns)
```
R = 100 × ln(P_final / P_initial)

Example: $10,000 → $11,250
R = 100 × ln(11250/10000) = 11.78
```

### Agent Confidence
```
Buy Signal:
  Conf = (RSI_strength + MACD_strength) / 2
  Range: [0, 1]
  
Sell Signal:
  Conf = (2 - RSI_strength - MACD_strength) / 2
```

### Portfolio Value
```
Each Step:
  V = Cash + (Position × Price)
  
Example: Cash=$5000, Shares=5, Price=$100
  V = 5000 + (5 × 100) = $5500
```

---

## 🌐 Real-World Data Sources

### Free Price Data
```python
# yfinance (Yahoo Finance)
import yfinance as yf
data = yf.download("AAPL", "2024-01-01", "2024-12-31")
prices = data['Close'].values.tolist()

# Alpaca (US Stocks)
from alpaca_trade_api import REST
api = REST()
bars = api.get_barset('AAPL', 'day', limit=500)

# Crypto (CCXT)
import ccxt
binance = ccxt.binance()
ohlcv = binance.fetch_ohlcv('BTC/USDT', '1d', limit=500)
prices = [x[4] for x in ohlcv]  # closing prices
```

### Environment Variables
```bash
# Set once, use in code
$env:MONGODB_URI = "mongodb://localhost:27017"
$env:API_PORT = "8000"
$env:LOG_LEVEL = "INFO"

# Check in Python
import os
uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
```

---

## 📚 Documentation Links

| Topic | File |
|-------|------|
| Full Setup | [README.md](README.md) |
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Quick Ref | [QUICKREF.md](QUICKREF.md) (this) |
| API Docs | http://localhost:8000/docs |
| Config | [config.py](config.py) |

---

## ⚡ Pro Tips

1. **Save session results after completion**
   ```python
   resp = requests.get(f"http://localhost:8000/replay/{session_id}")
   import json
   with open(f"{session_id}.json", "w") as f:
       json.dump(resp.json(), f, indent=2)
   ```

2. **Compare multiple training runs**
   ```python
   sessions = requests.get("http://localhost:8000/sessions?limit=50").json()
   best = max(sessions['sessions'], key=lambda x: x['total_return'])
   ```

3. **Export to analysis tools**
   ```python
   import pandas as pd
   session = requests.get(f"/replay/{sid}").json()
   df = pd.DataFrame(session['steps'])
   df.to_csv("trading_log.csv")
   ```

4. **Monitor GPU usage (if using CUDA)**
   ```bash
   nvidia-smi --loop=1  # Updates every second
   ```

5. **Enable verbose logging**
   ```python
   # config.py
   class RLModelConfig:
       VERBOSE = 2  # 0=none, 1=normal, 2=detailed
   ```

---

## 🎓 Learning Path

**Day 1: Setup & Basics**
- [ ] Install dependencies
- [ ] Run `example.py`
- [ ] Check API docs
- [ ] Train on synthetic data

**Day 2: Customization**
- [ ] Modify `config.py`
- [ ] Experiment with parameters
- [ ] Train multiple models
- [ ] Compare results

**Day 3: Integration**
- [ ] Connect real price data
- [ ] Build analysis script
- [ ] Create visualization
- [ ] Document findings

**Week 2+: Production**
- [ ] Deploy to cloud
- [ ] Setup monitoring
- [ ] Implement backtesting
- [ ] Scale to multiple assets

---

## 📞 Quick Help

```bash
# Check Python version
python --version  # Need 3.10+

# Check MongoDB
mongo --version

# Test API running
curl http://localhost:8000/health

# View API docs
# Open browser: http://localhost:8000/docs

# Kill stuck processes
taskkill /IM pythonw.exe /F
```

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Author**: RL Trading Agent Team

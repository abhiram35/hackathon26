# RL Trading Agent Backend

A modular FastAPI backend for a Reinforcement Learning trading agent using PPO (Proximal Policy Optimization) from stable-baselines3. The system features async MongoDB integration, custom Gymnasium environment with technical indicators, and real-time confidence scoring.

## Architecture

```
┌─────────────────────────────────────────────────┐
│          FastAPI Web Server (main.py)           │
│  - POST /train: Start training sessions         │
│  - GET /replay/{id}: Fetch completed sessions   │
└────────────┬────────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────▼──────┐  ┌──▼─────────────┐
│ TradingEnv │  │ Motor (Async    │
│ (Gymnasium)│  │ MongoDB Driver) │
│ - Obs: Box │  │ - Sessions      │
│ - Act: 3   │  │ - Steps Log     │
│ - Reward:  │  │ - Model Metrics │
│   LogRet   │  └─────────────────┘
│ - Confiden │
│   ce Score │
└────────────┘
```

## Components

### 1. **database.py** - Data Layer
- **MongoDBClient**: Async MongoDB wrapper using Motor
- **TradingSession**: Pydantic model for complete trading sessions
- **TradeStep**: Schema for individual steps with:
  - `timestamp`: Step index
  - `price`: Current market price
  - `action`: Action taken (0=Sell, 1=Hold, 2=Buy)
  - `reward`: Step reward from log returns
  - `agent_confidence`: Saliency/confidence score [0, 1]

**Key Methods**:
- `create_session()`: Store new session
- `add_step()`: Log trade steps
- `get_session()`: Retrieve by ID
- `update_session()`: Update metrics
- `get_all_sessions()`: Query with filters

### 2. **environment.py** - RL Environment
Custom Gymnasium environment for trading with:

**Observation Space**:
- 20-step price window (normalized to [0, 1])
- RSI (14-period): [0, 1]
- MACD Histogram: [0, 1]
- Volume Indicator: [0, 1]
- Portfolio Value: [0, 1]
- **Total: 24-dimensional observation**

**Action Space**:
- `0`: Sell (short)
- `1`: Hold
- `2`: Buy (long)

**Reward Function**:
$$R_t = 100 \times \ln\left(\frac{V_t}{V_0}\right) - \text{penalties}$$

Where:
- $V_t$ = Portfolio value at time $t$
- $V_0$ = Initial balance
- Penalties for underwater positions and excessive trading

**Confidence Score**:
- Based on indicator alignment (RSI + MACD)
- Higher when price action aligns with technical indicators
- Useful for UI visualization of agent certainty

**Technical Indicators**:
- **RSI**: Relative Strength Index (momentum oscillator)
- **MACD**: Moving Average Convergence Divergence (trend following)
- **Volume Proxy**: Price change magnitude as volume indicator

### 3. **main.py** - FastAPI Backend

#### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check with DB status |
| `POST` | `/train` | Start training session (async) |
| `GET` | `/replay/{session_id}` | Fetch completed session |
| `GET` | `/sessions` | List all sessions with stats |
| `GET` | `/sessions/{session_id}/stats` | Detailed analytics |
| `DELETE` | `/sessions/{session_id}` | Delete session |

#### POST /train

**Request**:
```json
{
  "episodes": 100,
  "total_timesteps": 10000,
  "price_data": [100.0, 101.5, 99.2, ...],
  "initial_balance": 10000.0,
  "session_name": "SPY_Jan2024"
}
```

**Response** (202 Accepted):
```json
{
  "session_id": "abc123...",
  "status": "queued",
  "message": "Training session queued..."
}
```

Training runs in background. Check status with GET /replay/{session_id}.

#### GET /replay/{session_id}

**Response**:
```json
{
  "session_id": "abc123...",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:45:00",
  "initial_balance": 10000.0,
  "final_balance": 11250.50,
  "total_return": 0.1251,
  "num_steps": 500,
  "status": "completed",
  "steps": [
    {
      "timestamp": 0,
      "price": 100.5,
      "action": 2,
      "reward": 0.05,
      "agent_confidence": 0.87,
      "observation": [...]
    },
    ...
  ]
}
```

## Setup

### Prerequisites
- Python 3.10+
- MongoDB 4.4+ (local or cloud)
- pip/conda

### Installation

1. **Clone and navigate**:
```bash
cd "c:\Users\Abhiram\OneDrive\Documents\Hackathon"
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start MongoDB** (if local):
```bash
# Windows: MongoDB should be running as service
# Or run: mongod --dbpath <path>
mongod --dbpath "C:\data\db"
```

5. **Set environment variables**:
```bash
# PowerShell
$env:MONGODB_URI = "mongodb://localhost:27017"

# Or for MongoDB Atlas:
$env:MONGODB_URI = "mongodb+srv://<user>:<pass>@cluster.mongodb.net/trading_agent"
```

### Running the Server

```bash
# Development (with auto-reload)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access API docs at: `http://localhost:8000/docs`

## Usage Examples

### Example 1: Train on Historic Price Data

```python
import requests
import numpy as np

# Generate synthetic price data
prices = np.cumsum(np.random.randn(1000)) + 100
prices = prices.astype(float).tolist()

# Start training
response = requests.post("http://localhost:8000/train", json={
    "price_data": prices,
    "initial_balance": 10000.0,
    "total_timesteps": 5000,
    "session_name": "Synthetic_Data_Run"
})

session_id = response.json()["session_id"]
print(f"Training started: {session_id}")

# Poll for completion
import time
while True:
    result = requests.get(f"http://localhost:8000/replay/{session_id}")
    data = result.json()
    
    if data["status"] == "completed":
        print(f"\n✅ Training completed!")
        print(f"Final balance: ${data['final_balance']:.2f}")
        print(f"Total return: {data['total_return']*100:.2f}%")
        print(f"Steps taken: {data['num_steps']}")
        break
    else:
        print(f"Status: {data['status']}")
        time.sleep(5)
```

### Example 2: Analyze Agent Confidence

```python
import requests

session_id = "your_session_id"
response = requests.get(f"http://localhost:8000/replay/{session_id}")
session = response.json()

# Analyze confidence scores
confidences = [step["agent_confidence"] for step in session["steps"]]
actions = [step["action"] for step in session["steps"]]

# Map actions
action_names = {0: "SELL", 1: "HOLD", 2: "BUY"}

# High confidence trades
high_confidence_trades = [
    (i, actions[i], confidences[i])
    for i in range(len(confidences))
    if confidences[i] > 0.8
]

print(f"High confidence trades (>0.8):")
for step, action, conf in high_confidence_trades[:10]:
    print(f"  Step {step}: {action_names[action]} (confidence: {conf:.2%})")
```

### Example 3: List and Compare Sessions

```python
import requests
from datetime import datetime

response = requests.get("http://localhost:8000/sessions?limit=10")
data = response.json()

print(f"Total sessions: {data['total_sessions']}")
print(f"Completed: {data['completed_sessions']}")
print(f"Average return: {data['avg_return']*100:.2f}%\n")

# Sort by return
sessions = sorted(data["sessions"], key=lambda x: x["total_return"], reverse=True)

print("Top 5 performing sessions:")
for session in sessions[:5]:
    created = datetime.fromisoformat(session["created_at"])
    return_pct = session["total_return"] * 100
    print(f"  {session['session_id'][:8]}... | Return: {return_pct:+.2f}% | Steps: {session['num_steps']}")
```

## Technical Details

### Reward Calculation

The environment uses **log returns** to calculate rewards:

```python
log_return = ln(portfolio_value / initial_balance)
reward = 100 * log_return
```

**Why log returns?**
- Scale-invariant (works with any portfolio size)
- Mathematically tractable for differential rewards
- Natural for compound growth calculations

**Additional penalties**:
- Underwater positions: -0.5 reward
- Excessive trading: -0.1 per trade

### Confidence/Saliency Score

The agent's confidence reflects how aligned technical indicators are with its action:

```
For Buy signal:
  confidence = (RSI_bullish + MACD_bullish) / 2

For Sell signal:
  confidence = (1 - RSI_bullish + 1 - MACD_bullish) / 2

For Hold:
  confidence = 0.5 (neutral)
```

Where:
- `RSI_bullish = 1.0` if RSI > 0.7, `0.0` if RSI < 0.3, else `0.5`
- `MACD_bullish` = similarity using MACD crossover

### PPO Training

The model uses **Proximal Policy Optimization** with:
- Learning rate: 3e-4
- Batch size: 64
- Optimization epochs: 10
- Gamma (discount): 0.99
- GAE lambda: 0.95
- Clip range: 0.2

Adjust these in `main.py`'s `train_agent_background()` function.

## Performance Tips

1. **Price Data**: 500+ points recommended for meaningful training
2. **Window Size**: 20-period window balances context and computation
3. **Transaction Costs**: 0.1% mimics real market conditions
4. **Total Timesteps**: Start with 10,000-50,000 for quick experimentation

## Database Schema

MongoDB collections automatically created:

**trading_sessions**
```javascript
{
  _id: ObjectId,
  session_id: String (unique),
  created_at: Date,
  completed_at: Date,
  status: String ["queued", "training", "completed", "failed"],
  initial_balance: Number,
  final_balance: Number,
  total_return: Number,
  episode_reward: Number,
  num_steps: Number,
  model_version: String,
  steps: Array [
    {
      timestamp: Number,
      price: Number,
      action: Number,
      reward: Number,
      agent_confidence: Number,
      observation: Array
    }
  ]
}
```

Indexes:
- `session_id` (unique)
- `created_at` (for time-range queries)
- `status` (for filtering)

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t rl-trader .
docker run -p 8000:8000 -e MONGODB_URI="mongodb://mongo:27017" rl-trader
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGODB_DB` | `trading_agent` | Database name |

## Troubleshooting

### MongoDB Connection Error
```
Error: Database not initialized
```
**Solution**: Ensure MongoDB is running and MONGODB_URI is correct.

### Out of Memory During Training
```
RuntimeError: CUDA out of memory
```
**Solution**:
- Reduce `n_steps` in PPO config
- Reduce `total_timesteps`
- Use CPU instead: `device='cpu'` in PPO init

### Slow Training
**Optimize**:
- Reduce observation space (use smaller window)
- Decrease price data resolution
- Use fewer training epochs

## Future Enhancements

- [ ] Multiple agent architectures (PPO, A2C, DQN)
- [ ] Live market data integration
- [ ] Ensemble trading strategies
- [ ] Real-time backtesting engine
- [ ] WebSocket for live confidence scores
- [ ] Multi-asset portfolio optimization
- [ ] Risk metrics (Sharpe ratio, Sortino ratio)

## License

MIT

## Support

For issues or questions, check:
1. MongoDB is running
2. All dependencies installed: `pip install -r requirements.txt`
3. API docs: `http://localhost:8000/docs`
4. Logs in terminal output during training

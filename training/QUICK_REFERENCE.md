# Agent Training - Quick Reference

## 🚀 Quick Start Commands

### Interactive Training (Easiest)
```bash
python scripts/train_scenarios.py
# Select from 8 pre-built scenarios
```

### Basic Training (5 lines)
```python
from scripts.agent import RLTradingAgent
agent = RLTradingAgent(verbose=1)
agent.create_environment(); agent.create_model()
agent.train(total_timesteps=50000); agent.save_model("agent")
```

---

## 📋 Agent Class API

### Initialization
```python
RLTradingAgent(
    config=None,           # Config object
    model_type="PPO",      # "PPO", "DQN", "A2C"
    device="auto",         # "cpu", "cuda", "auto"
    verbose=1,             # 0-2 verbosity level
)
```

### Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `create_environment()` | Create trading environment | env |
| `create_model()` | Initialize RL model | model |
| `train()` | Train agent | history |
| `evaluate()` | Test agent performance | metrics |
| `save_model()` | Save trained model | path |
| `load_model()` | Load pre-trained model | model |
| `predict()` | Get action for observation | action |
| `reset()` | Reset environment | obs |
| `close()` | Cleanup resources | None |

---

## 🎯 Common Workflows

### 1️⃣ Default Training
```python
from scripts.agent import RLTradingAgent

agent = RLTradingAgent(verbose=1)
agent.create_environment()
agent.create_model()
agent.train(total_timesteps=50000)
agent.evaluate(n_episodes=10)
agent.save_model("my_agent")
agent.close()
```

### 2️⃣ Compare Algorithms
```python
from scripts.train_scenarios import compare_algorithms
results = compare_algorithms()
```

### 3️⃣ Fine-tune Model
```python
agent = RLTradingAgent(verbose=1)
agent.create_environment()
agent.load_model("models/agent.zip")
agent.model.learning_rate = 1e-5
agent.train(total_timesteps=25000)
agent.save_model("finetuned")
```

### 4️⃣ Test Different Presets
```python
for preset in ["conservative", "balanced", "aggressive"]:
    agent = RLTradingAgent()
    agent.create_environment(config_preset=preset)
    agent.create_model()
    agent.train(total_timesteps=50000)
    agent.evaluate(n_episodes=5)
    agent.save_model(f"agent_{preset}")
    agent.close()
```

### 5️⃣ Hyperparameter Search
```python
for lr in [1e-4, 3e-4, 1e-3]:
    agent = RLTradingAgent()
    agent.create_environment()
    agent.create_model(learning_rate=lr)
    agent.train(total_timesteps=50000)
    print(f"LR {lr}: {agent.evaluate(5)['mean_reward']:.2f}")
    agent.close()
```

---

## ⚙️ Configuration Presets

### Conservative
```python
agent.create_environment(config_preset="conservative")
# Suitable for: Capital preservation, lower risk
# Features: 1x leverage, 2% risk limit
```

### Balanced (Default)
```python
agent.create_environment(config_preset="balanced")
# Suitable for: Most trading strategies
# Features: 2x leverage, 5% risk limit
```

### Aggressive
```python
agent.create_environment(config_preset="aggressive")
# Suitable for: Growth strategies, higher risk tolerance
# Features: 3x leverage, 10% risk limit
```

---

## 🤖 Algorithm Comparison

| Algorithm | Speed | Stability | Memory | Best For |
|-----------|-------|-----------|--------|----------|
| **PPO** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **Recommended** |
| **DQN** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Discrete actions |
| **A2C** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Fast training |

### Usage
```python
agent = RLTradingAgent(model_type="PPO")   # ← Start here
agent = RLTradingAgent(model_type="DQN")   # Alternative
agent = RLTradingAgent(model_type="A2C")   # Faster
```

---

## 📊 Training Parameters

### Typical Training
```python
agent.train(
    total_timesteps=100000,      # Steps to train
    checkpoint_interval=10000,   # Save every N steps
    callback_verbose=1           # Log verbosity
)
```

### Quick Testing
```python
agent.train(total_timesteps=10000, checkpoint_interval=5000)
```

### Long Training
```python
agent.train(total_timesteps=500000, checkpoint_interval=50000)
```

---

## 📈 Evaluation Metrics

```python
metrics = agent.evaluate(n_episodes=10)

# Access metrics:
metrics['mean_reward']      # Average reward per episode
metrics['std_reward']       # Standard deviation
metrics['max_reward']       # Best episode reward
metrics['min_reward']       # Worst episode reward
metrics['mean_length']      # Avg steps per episode
```

### Interpret Results
```
Mean Reward > 0  → Agent making profit ✅
Std < Mean/2     → Consistent performance ✅
Max > Min*2      → Variable across episodes ⚠️
```

---

## 💾 Model Management

### Save
```python
path = agent.save_model("my_agent")
# Saves to: training/models/my_agent_<timestamp>.zip
```

### Load
```python
agent.load_model("training/models/my_agent_123456.zip")
```

### List Models
```python
from pathlib import Path
models = list(Path("training/models").glob("*.zip"))
for m in models: print(m.name)
```

### Delete Old Models
```python
import os
model_dir = Path("training/models")
for m in list(model_dir.glob("*.zip"))[:-5]:  # Keep 5 recent
    os.remove(m)
```

---

## 🔍 Monitoring

### View Logs in TensorBoard
```bash
tensorboard --logdir=training/logs/
# Visit: http://localhost:6006
```

### Check Progress
```python
# In training loop, automatically logs:
# - Episode reward
# - Episode length
# - Learning rate
# - Loss values
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Environment not created" | Call `create_environment()` first |
| GPU out of memory | Use `device="cpu"` |
| Slow training | Reduce `total_timesteps` or dataset size |
| Model won't improve | Increase `learning_rate` or try different algorithm |
| Module not found | Install: `pip install -r requirements.txt` |

---

## 📁 File Structure

```
training/
├── scripts/
│   ├── agent.py          ← Main agent class
│   ├── train_scenarios.py ← Pre-built scenarios
│   ├── train.py          ← Original training script
│   ├── evaluate.py       ← Evaluation utils
│   └── data_utils.py     ← Data loading
├── models/               ← Saved models
├── logs/                 ← TensorBoard logs
├── data/                 ← Training data (CSV)
├── requirements.txt      ← Dependencies
└── TRAINING_GUIDE.md     ← Full guide
```

---

## ✅ Checklist

Before training:
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Backend running: `python backend/main.py`
- [ ] Output directories exist (auto-created)
- [ ] Data available (synthetic if needed)
- [ ] GPU available (optional): `nvidia-smi`

---

## 🎓 Examples by Complexity

### Beginner (Just run it)
```bash
python scripts/train_scenarios.py
# Pick scenario 1
```

### Intermediate (Customize)
```python
agent = RLTradingAgent(model_type="DQN")
agent.create_environment(config_preset="aggressive")
agent.create_model(learning_rate=5e-4)
agent.train(total_timesteps=100000)
agent.evaluate(n_episodes=10)
```

### Advanced (Full control)
```python
# Custom environment, algorithm tuning, callbacks
from scripts.agent import RLTradingAgent

agent = RLTradingAgent(verbose=2)
prices = load_custom_data("data.csv")
agent.create_environment(prices=prices)
agent.create_model(learning_rate=1e-4)
agent.train(total_timesteps=250000)
metrics = agent.evaluate(n_episodes=20)
agent.save_model(f"v{metrics['mean_reward']:.2f}")
```

---

## 🚀 Next Steps

1. **Now**: Run `python scripts/train_scenarios.py` → Pick scenario 1
2. **Then**: Explore different presets (conservative/aggressive)
3. **Next**: Compare algorithms to find best fit
4. **Finally**: Fine-tune hyperparameters for your data

---

**Need help?** Read `TRAINING_GUIDE.md` for detailed documentation.

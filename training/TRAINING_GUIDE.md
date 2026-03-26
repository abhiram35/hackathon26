# RL Trading Agent Training Guide

## 📚 Overview

You now have two powerful files for agent training:

1. **`agent.py`** - Core agent class with full training pipeline
2. **`train_scenarios.py`** - Pre-built training scenarios with examples

## 🚀 Quick Start

### Installation

```bash
cd training
pip install -r requirements.txt
```

### Basic Training (5 lines of code)

```python
from scripts.agent import RLTradingAgent

# Create and train
agent = RLTradingAgent(model_type="PPO", verbose=1)
agent.create_environment(config_preset="balanced")
agent.create_model(learning_rate=3e-4)
agent.train(total_timesteps=50000)
agent.save_model("my_agent")
```

## 📖 Detailed Usage

### 1. Import the Agent Class

```python
from scripts.agent import RLTradingAgent
from config import Config
```

### 2. Initialize Agent

```python
agent = RLTradingAgent(
    model_type="PPO",      # "PPO", "DQN", or "A2C"
    device="cpu",          # "cpu", "cuda", or "auto"
    verbose=1,             # 0=silent, 1=info, 2=debug
)
```

### 3. Create Environment

#### With Synthetic Data (Default)
```python
agent.create_environment(config_preset="balanced")
# Presets: "conservative", "balanced", "aggressive"
```

#### With Custom Price Data
```python
import numpy as np
prices = np.random.randn(252, 5) + 100  # OHLCV format
agent.create_environment(prices=prices)
```

#### With Real CSV Data
```python
from scripts.data_utils import load_price_data
prices = load_price_data("path/to/prices.csv")
agent.create_environment(prices=prices)
```

### 4. Create Model

```python
agent.create_model(
    learning_rate=3e-4,
    policy="MlpPolicy"     # "MlpPolicy" or "CnnPolicy"
)
```

### 5. Train the Agent

```python
agent.train(
    total_timesteps=100000,
    checkpoint_interval=10000,
    callback_verbose=1
)
```

### 6. Evaluate Performance

```python
metrics = agent.evaluate(
    n_episodes=10,
    render=False
)

print(f"Mean Reward: {metrics['mean_reward']:.2f}")
print(f"Max Reward: {metrics['max_reward']:.2f}")
```

### 7. Save and Load Models

```python
# Save
model_path = agent.save_model("my_agent_v1")

# Load
agent.load_model(str(model_path))
```

### 8. Make Predictions

```python
obs, _ = agent.reset()
action = agent.predict(obs, deterministic=True)
```

## 🎯 Training Scenarios

### Run Interactive Menu

```bash
python scripts/train_scenarios.py
# Select a scenario from the menu
```

### Or Run Directly

```python
from scripts.train_scenarios import (
    train_default_agent,
    train_conservative_agent,
    compare_algorithms,
)

# Default training
agent, metrics = train_default_agent()

# Conservative training
agent, metrics = train_conservative_agent()

# Compare algorithms
results = compare_algorithms()
```

## 🔧 Configuration Guide

### Algorithm-Specific Parameters

#### PPO (Recommended for Trading)
```python
agent = RLTradingAgent(model_type="PPO")
agent.create_model(learning_rate=3e-4)

# PPO automatically configures:
# - n_steps: 2048 (trajectory length)
# - batch_size: 64 (training batch)
# - n_epochs: 10 (policy update iterations)
# - gamma: 0.99 (discount factor)
# - clip_range: 0.2 (policy clip parameter)
```

#### DQN (For Discrete Actions)
```python
agent = RLTradingAgent(model_type="DQN")
agent.create_model(learning_rate=1e-4)

# DQN automatically configures:
# - buffer_size: 10000 (experience replay buffer)
# - learning_starts: 1000 (when to start learning)
# - exploration_fraction: 0.1 (exploration period)
```

#### A2C (Fast & Simple)
```python
agent = RLTradingAgent(model_type="A2C")
agent.create_model(learning_rate=3e-4)

# A2C automatically configures:
# - n_steps: 5 (trajectory length)
# - gae_lambda: 0.95 (generalized advantage estimation)
```

### Environment Presets

#### Conservative (Low Risk)
- Initial Balance: $10,000
- Transaction Cost: 0.001 (0.1%)
- Leverage: 1x
- Risk Limit: 2% per trade

#### Balanced (Recommended)
- Initial Balance: $10,000
- Transaction Cost: 0.001 (0.1%)
- Leverage: 2x
- Risk Limit: 5% per trade

#### Aggressive (High Risk)
- Initial Balance: $10,000
- Transaction Cost: 0.001 (0.1%)
- Leverage: 3x
- Risk Limit: 10% per trade

## 📊 Training Examples

### Example 1: Simple Training

```python
from scripts.agent import RLTradingAgent

agent = RLTradingAgent(verbose=1)
agent.create_environment()
agent.create_model()
agent.train(total_timesteps=50000)
agent.evaluate(n_episodes=5)
agent.save_model("simple_agent")
agent.close()
```

### Example 2: Custom Configuration

```python
from scripts.agent import RLTradingAgent
from config import Config

# Custom config
config = Config()
config.initial_balance = 50000
config.transaction_cost = 0.0005

agent = RLTradingAgent(config=config, verbose=2)
agent.create_environment(config_preset="aggressive")
agent.create_model(learning_rate=5e-4)

agent.train(
    total_timesteps=200000,
    checkpoint_interval=50000
)

metrics = agent.evaluate(n_episodes=20)
print(f"Final Reward: {metrics['mean_reward']:.2f}")

agent.save_model("custom_agent")
agent.close()
```

### Example 3: Fine-tuning

```python
from scripts.agent import RLTradingAgent

# Create new agent
agent = RLTradingAgent(verbose=1)
agent.create_environment(config_preset="balanced")

# Load pre-trained model
agent.load_model("models/agent_PPO_20240101_120000.zip")

# Lower learning rate for fine-tuning
agent.model.learning_rate = 1e-5

# Train on new data
agent.train(total_timesteps=25000)
agent.evaluate(n_episodes=5)

agent.save_model("finetuned_agent")
agent.close()
```

### Example 4: Multi-Algorithm Comparison

```python
from scripts.agent import RLTradingAgent

algorithms = ["PPO", "DQN", "A2C"]
results = {}

for algo in algorithms:
    print(f"Training {algo}...")
    agent = RLTradingAgent(model_type=algo, verbose=0)
    agent.create_environment()
    agent.create_model()
    agent.train(total_timesteps=50000)
    
    metrics = agent.evaluate(n_episodes=10)
    results[algo] = metrics['mean_reward']
    
    agent.close()

# Print results
for algo, reward in results.items():
    print(f"{algo}: {reward:.2f}")
```

## 📈 Monitoring Training

### Real-time Plots

Training logs are saved in `training/logs/` directory. View with TensorBoard:

```bash
tensorboard --logdir=training/logs/
# Open http://localhost:6006
```

### Training Checkpoints

Models are automatically saved every `checkpoint_interval` steps:

```
training/models/
├── agent_1.zip
├── agent_2.zip
└── agent_final.zip
```

### Evaluation Metrics

```python
metrics = agent.evaluate(n_episodes=10)

print(f"Mean Reward: {metrics['mean_reward']:.2f}")
print(f"Std Reward: {metrics['std_reward']:.2f}")
print(f"Max Reward: {metrics['max_reward']:.2f}")
print(f"Min Reward: {metrics['min_reward']:.2f}")
print(f"Mean Episode Length: {metrics['mean_length']:.0f}")
```

## 🔍 Debugging

### Enable Debug Output

```python
agent = RLTradingAgent(verbose=2)  # Max verbosity
```

### Render Trading Visualization

```python
metrics = agent.evaluate(n_episodes=1, render=True)
```

### Check Model Parameters

```python
print(f"Model type: {agent.model_type}")
print(f"Parameters: {agent.model.num_parameters()}")
print(f"Environment: {agent.env}")
```

## 💾 Model Management

### List All Models

```python
from pathlib import Path

model_dir = Path("training/models")
for model_file in model_dir.glob("*.zip"):
    print(model_file.name)
```

### Load Latest Model

```python
from pathlib import Path

model_dir = Path("training/models")
latest_model = max(model_dir.glob("*.zip"), key=lambda p: p.stat().st_mtime)
agent.load_model(str(latest_model))
```

## 🚀 Advanced Usage

### Custom Callbacks

```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    def _on_step(self):
        # Called after every step
        if self.num_timesteps % 1000 == 0:
            print(f"Steps: {self.num_timesteps}")
        return True

# Use in training
agent.train(total_timesteps=100000)
```

### Hyperparameter Grid Search

```python
from itertools import product

learning_rates = [1e-4, 3e-4, 1e-3]
batch_sizes = [32, 64, 128]

results = {}
for lr, bs in product(learning_rates, batch_sizes):
    agent = RLTradingAgent(verbose=0)
    agent.create_environment()
    agent.create_model(learning_rate=lr)
    agent.train(total_timesteps=50000)
    
    metrics = agent.evaluate(n_episodes=5)
    results[(lr, bs)] = metrics['mean_reward']
    agent.close()

# Find best params
best_params = max(results, key=results.get)
print(f"Best params: lr={best_params[0]}, bs={best_params[1]}")
```

### Multi-objective Optimization

```python
# Maximize return while minimizing risk
agent.train(total_timesteps=100000)
metrics = agent.evaluate(n_episodes=20)

sharpe_ratio = metrics['mean_reward'] / metrics['std_reward']
max_drawdown = abs(metrics['min_reward'])

print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Max Drawdown: {max_drawdown:.2f}%")
```

## 📋 Checklist Before Training

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify backend is running: `python backend/main.py`
- [ ] Have MongoDB available (local or cloud)
- [ ] Check GPU availability (optional but recommended)
- [ ] Prepare data (synthetic or real CSV)
- [ ] Set hyperparameters
- [ ] Create output directories (done automatically)

## 🐛 Common Issues

### Issue: "Environment not created"
```python
# FIX: Call create_environment before create_model
agent.create_environment()
agent.create_model()
```

### Issue: CUDA out of memory
```python
# FIX: Use CPU instead
agent = RLTradingAgent(device="cpu")
```

### Issue: Very slow training
```python
# FIX: Use fewer episodes or reduce dataset size
agent.train(total_timesteps=10000)
```

## 📚 Further Reading

- Stable Baselines3 Docs: https://stable-baselines3.readthedocs.io/
- Gymnasium Docs: https://gymnasium.farama.org/
- RL Trading: https://openai.com/research

## 🎓 Learning Path

1. **Start**: Run `train_scenarios.py` → Scenario 1 (Default)
2. **Explore**: Try different presets (conservative, aggressive)
3. **Compare**: Run algorithm comparison (PPO vs DQN vs A2C)
4. **Optimize**: Tune hyperparameters for your use case
5. **Deploy**: Save best model and use in production

---

**Happy Training! 🚀📈**

For questions or issues, check the `IMPLEMENTATION_GUIDE.md` in the frontend folder.

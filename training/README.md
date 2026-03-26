# RL Trading Agent - Training

Standalone training scripts for the RL trading agent.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create sample data
python scripts/data_utils.py
```

## Training

### Basic Training

```bash
# Train with sample data
python scripts/train.py --data data/sample_prices.csv --timesteps 10000 --output models/ppo_model.zip

# Train with custom parameters
python scripts/train.py \
    --data data/your_prices.csv \
    --timesteps 50000 \
    --balance 50000 \
    --evaluate \
    --episodes 10
```

### Evaluation

```bash
# Evaluate trained model
python scripts/evaluate.py models/ppo_model.zip --data data/sample_prices.csv --episodes 5

# Generate evaluation plots
python scripts/evaluate.py models/ppo_model.zip --data data/sample_prices.csv --plot
```

## File Structure

- `scripts/train.py` - Main training script
- `scripts/evaluate.py` - Model evaluation and visualization
- `scripts/data_utils.py` - Data generation and loading utilities
- `data/` - Price data directory
- `models/` - Trained model storage

## Data Format

Price data should be a CSV file with one price per line:
```
100.5
101.2
99.8
102.3
...
```

Or with headers (will use first column):
```
date,close
2024-01-01,100.5
2024-01-02,101.2
...
```

## Training Parameters

- `--timesteps`: Total training steps (default: 10000)
- `--balance`: Initial balance in dollars (default: 10000)
- `--data`: Path to price data file
- `--output`: Where to save trained model
- `--evaluate`: Run evaluation after training
- `--episodes`: Number of evaluation episodes

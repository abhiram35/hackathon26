"""
Training script for RL trading agent.
Supports standalone training with price data files.
"""

import sys
import os
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym

from environment import TradingEnv
from config import TrainingConfig, EnvironmentConfig, RLModelConfig


def load_price_data(filepath):
    """Load price data from CSV or text file."""
    try:
        data = np.loadtxt(filepath, delimiter=',', dtype=float)
        if data.ndim == 2:
            data = data[:, 0]  # Use first column if multiple columns
        return data
    except Exception as e:
        print(f"Error loading price data: {e}")
        return None


def train_agent(
    price_data,
    total_timesteps=10000,
    initial_balance=10000.0,
    output_path=None,
    verbose=1
):
    """
    Train RL agent on trading environment.
    
    Args:
        price_data: Array of historical prices
        total_timesteps: Total training timesteps
        initial_balance: Starting capital
        output_path: Where to save the trained model
        verbose: Verbosity level
        
    Returns:
        Trained PPO model
    """
    print(f"\n{'='*60}")
    print(f"Training RL Trading Agent")
    print(f"{'='*60}")
    print(f"Timesteps: {total_timesteps:,}")
    print(f"Initial Balance: ${initial_balance:,.2f}")
    print(f"Price Data Points: {len(price_data):,}")
    print(f"{'='*60}\n")
    
    # Create environment
    env = TradingEnv(
        price_data=price_data,
        initial_balance=initial_balance,
        window_size=EnvironmentConfig.WINDOW_SIZE,
        transaction_cost=EnvironmentConfig.TRANSACTION_COST,
    )
    
    # Wrap in DummyVecEnv
    vec_env = DummyVecEnv([lambda: env])
    
    # Create PPO agent
    model = PPO(
        RLModelConfig.POLICY_TYPE,
        vec_env,
        learning_rate=RLModelConfig.LEARNING_RATE,
        n_steps=RLModelConfig.N_STEPS,
        batch_size=RLModelConfig.BATCH_SIZE,
        n_epochs=RLModelConfig.N_EPOCHS,
        gamma=RLModelConfig.GAMMA,
        gae_lambda=RLModelConfig.GAE_LAMBDA,
        clip_range=RLModelConfig.CLIP_RANGE,
        verbose=verbose,
    )
    
    print("Starting training...\n")
    
    # Train
    model.learn(
        total_timesteps=total_timesteps,
        progress_bar=True,
    )
    
    # Save model
    if output_path:
        model.save(output_path)
        print(f"\n✅ Model saved to: {output_path}")
    
    vec_env.close()
    
    return model


def evaluate_agent(model, env, num_episodes=5):
    """
    Evaluate trained agent on environment.
    
    Args:
        model: Trained PPO model
        env: Trading environment
        num_episodes: Number of evaluation episodes
        
    Returns:
        List of episode returns
    """
    print(f"\n{'='*60}")
    print(f"Evaluating Agent")
    print(f"{'='*60}\n")
    
    returns = []
    
    for episode in range(num_episodes):
        obs, _ = env.reset()
        episode_return = 0.0
        done = False
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_return += reward
            done = terminated or truncated
        
        returns.append(episode_return)
        portfolio_value = env.get_portfolio_value()
        total_return = (portfolio_value - env.initial_balance) / env.initial_balance
        
        print(f"Episode {episode + 1}: Return={episode_return:.2f}, Portfolio=${portfolio_value:,.2f} ({total_return*100:+.2f}%)")
    
    avg_return = np.mean(returns)
    print(f"\nAverage Return: {avg_return:.2f}")
    
    return returns


def main():
    parser = argparse.ArgumentParser(description='Train RL trading agent')
    parser.add_argument('--data', type=str, default='data/prices.csv', help='Path to price data file')
    parser.add_argument('--timesteps', type=int, default=10000, help='Total training timesteps')
    parser.add_argument('--balance', type=float, default=10000.0, help='Initial balance')
    parser.add_argument('--output', type=str, default=None, help='Output model path')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate after training')
    parser.add_argument('--episodes', type=int, default=5, help='Evaluation episodes')
    
    args = parser.parse_args()
    
    # Load price data
    print(f"Loading price data from: {args.data}")
    price_data = load_price_data(args.data)
    
    if price_data is None:
        print("❌ Failed to load price data")
        return
    
    # Generate default output path if not specified
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent / 'models'
        output_dir.mkdir(exist_ok=True)
        args.output = os.path.join(output_dir, f"ppo_trading_{timestamp}.zip")
    
    # Train agent
    model = train_agent(
        price_data,
        total_timesteps=args.timesteps,
        initial_balance=args.balance,
        output_path=args.output,
    )
    
    # Evaluate if requested
    if args.evaluate:
        env = TradingEnv(price_data, initial_balance=args.balance)
        evaluate_agent(model, env, num_episodes=args.episodes)


if __name__ == '__main__':
    main()

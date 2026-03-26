"""
Evaluation script for trained models.
"""

import sys
import os
import argparse
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from stable_baselines3 import PPO
from environment import TradingEnv
import matplotlib.pyplot as plt


def evaluate_model(model_path, price_data, initial_balance=10000.0, num_episodes=5):
    """
    Evaluate a trained model.
    
    Args:
        model_path: Path to saved model
        price_data: Array of price data
        initial_balance: Starting capital
        num_episodes: Number of episodes to evaluate
        
    Returns:
        Dictionary with evaluation results
    """
    print(f"\nLoading model from: {model_path}")
    model = PPO.load(model_path)
    
    env = TradingEnv(price_data, initial_balance=initial_balance)
    
    results = {
        'returns': [],
        'portfolio_values': [],
        'trades': [],
        'avg_return': 0.0,
        'avg_portfolio': 0.0,
        'total_trades': 0,
    }
    
    print(f"\n{'='*60}")
    print(f"Evaluating Model")
    print(f"{'='*60}\n")
    
    for episode in range(num_episodes):
        obs, _ = env.reset()
        episode_return = 0.0
        final_portfolio = 0.0
        done = False
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_return += reward
            final_portfolio = info['portfolio_value']
            done = terminated or truncated
        
        total_return = (final_portfolio - initial_balance) / initial_balance
        results['returns'].append(episode_return)
        results['portfolio_values'].append(final_portfolio)
        results['trades'].append(len(env.trades))
        
        print(f"Episode {episode + 1}:")
        print(f"  Reward: {episode_return:.2f}")
        print(f"  Portfolio: ${final_portfolio:,.2f}")
        print(f"  Return: {total_return*100:+.2f}%")
        print(f"  Trades: {len(env.trades)}")
    
    results['avg_return'] = np.mean(results['returns'])
    results['avg_portfolio'] = np.mean(results['portfolio_values'])
    results['total_trades'] = int(np.sum(results['trades']))
    
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"Avg Reward: {results['avg_return']:.2f}")
    print(f"Avg Portfolio Value: ${results['avg_portfolio']:,.2f}")
    print(f"Total Trades: {results['total_trades']}")
    print(f"Avg Return: {((results['avg_portfolio'] - initial_balance) / initial_balance)*100:+.2f}%")
    
    return results


def plot_results(model_path, price_data, initial_balance=10000.0):
    """Plot evaluation results."""
    print(f"\nLoading model from: {model_path}")
    model = PPO.load(model_path)
    
    env = TradingEnv(price_data, initial_balance=initial_balance)
    obs, _ = env.reset()
    
    actions = []
    prices = []
    portfolio_values = []
    done = False
    
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        actions.append(action)
        prices.append(info['price'])
        portfolio_values.append(info['portfolio_value'])
        done = terminated or truncated
    
    # Create plots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Price chart
    axes[0].plot(prices, label='Price', color='blue')
    axes[0].set_ylabel('Price')
    axes[0].set_title('Stock Price')
    axes[0].legend()
    axes[0].grid(True)
    
    # Portfolio value
    axes[1].plot(portfolio_values, label='Portfolio Value', color='green')
    axes[1].axhline(y=initial_balance, color='red', linestyle='--', label='Initial Balance')
    axes[1].set_ylabel('Value ($)')
    axes[1].set_title('Portfolio Value Over Time')
    axes[1].legend()
    axes[1].grid(True)
    
    # Actions
    axes[2].scatter(range(len(actions)), actions, c=actions, cmap='RdYlGn', s=50)
    axes[2].set_ylabel('Action')
    axes[2].set_title('Actions (0=Sell, 1=Hold, 2=Buy)')
    axes[2].set_ylim(-0.5, 2.5)
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('evaluation_results.png', dpi=100)
    print("✅ Results saved to evaluation_results.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained model')
    parser.add_argument('model', type=str, help='Path to saved model')
    parser.add_argument('--data', type=str, default='data/prices.csv', help='Path to price data')
    parser.add_argument('--balance', type=float, default=10000.0, help='Initial balance')
    parser.add_argument('--episodes', type=int, default=5, help='Number of episodes')
    parser.add_argument('--plot', action='store_true', help='Plot results')
    
    args = parser.parse_args()
    
    # Load price data
    try:
        price_data = np.loadtxt(args.data, delimiter=',', dtype=float)
        if price_data.ndim == 2:
            price_data = price_data[:, 0]
    except Exception as e:
        print(f"Error loading price data: {e}")
        return
    
    # Evaluate
    evaluate_model(args.model, price_data, args.balance, args.episodes)
    
    if args.plot:
        plot_results(args.model, price_data, args.balance)


if __name__ == '__main__':
    main()

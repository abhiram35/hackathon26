"""
Data utilities for training.
Generate sample data or load historical prices.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_synthetic_prices(num_points=500, start_price=100, volatility=0.02, drift=0.0001):
    """
    Generate synthetic price data using geometric Brownian motion.
    
    Args:
        num_points: Number of price points
        start_price: Initial price
        volatility: Daily volatility (std dev of returns)
        drift: Daily drift (mean return)
        
    Returns:
        Array of prices
    """
    dt = 1 / 252  # Daily time step
    prices = [start_price]
    
    for _ in range(num_points - 1):
        dW = np.random.normal(0, np.sqrt(dt))
        returns = drift * dt + volatility * dW
        new_price = prices[-1] * np.exp(returns)
        prices.append(new_price)
    
    return np.array(prices)


def load_csv_prices(filepath, column=0):
    """
    Load prices from CSV file.
    
    Args:
        filepath: Path to CSV file
        column: Column index to use (default 0)
        
    Returns:
        Array of prices
    """
    data = pd.read_csv(filepath)
    return data.iloc[:, column].values


def save_prices(prices, filepath):
    """Save prices to CSV file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(filepath, prices, delimiter=',', fmt='%.6f')
    print(f"✅ Prices saved to: {filepath}")


def create_sample_data():
    """Create sample price data for testing."""
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Generate sample prices
    prices = generate_synthetic_prices(num_points=1000)
    save_prices(prices, data_dir / 'sample_prices.csv')
    
    print(f"✅ Sample data created:")
    print(f"   Data points: {len(prices)}")
    print(f"   Price range: ${prices.min():.2f} - ${prices.max():.2f}")
    print(f"   File: {data_dir / 'sample_prices.csv'}")


if __name__ == '__main__':
    create_sample_data()

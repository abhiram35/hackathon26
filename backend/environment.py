"""
Custom Gymnasium environment for trading with RL agent.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Tuple, Dict, Any, Optional
from collections import deque
import warnings

warnings.filterwarnings("ignore")


class TradingEnv(gym.Env):
    """
    Custom trading environment for RL agent.
    
    Observation Space: Box space with normalized prices and 3 technical indicators
    - Window of last N normalized closing prices
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence) histogram
    - Volume indicator
    
    Action Space: Discrete(3)
    - 0: Sell (short)
    - 1: Hold
    - 2: Buy (long)
    """
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(
        self,
        price_data: np.ndarray,
        initial_balance: float = 10000.0,
        window_size: int = 20,
        transaction_cost: float = 0.001,  # 0.1% per trade
        max_steps: Optional[int] = None,
    ):
        """
        Initialize trading environment.
        
        Args:
            price_data: Array of historical prices
            initial_balance: Starting capital in dollars
            window_size: Size of price window for observation
            transaction_cost: Cost per transaction (as fraction)
            max_steps: Maximum steps per episode (defaults to len(price_data) - window_size)
        """
        self.price_data = np.array(price_data, dtype=np.float32)
        self.initial_balance = initial_balance
        self.window_size = window_size
        self.transaction_cost = transaction_cost
        self.max_steps = max_steps or len(self.price_data) - window_size - 1
        
        # State tracking
        self.current_step = 0
        self.balance = initial_balance
        self.initial_price = self.price_data[0]
        self.position = 0.0  # Current position in units held
        self.entry_price = 0.0  # Average entry price
        self.trades = []  # Track all trades for analysis
        self.episode_reward = 0.0
        self.last_action = 1  # Default: Hold
        
        # Technical indicators cache
        self._rsi_period = 14
        self._macd_fast = 12
        self._macd_slow = 26
        self._macd_signal = 9
        self._volume_period = 20
        
        # Define spaces
        # Observation: [window_size prices, RSI, MACD, Volume, Balance, Position]
        self.obs_size = window_size + 4  # 4 extra features (RSI, MACD, Volume, Portfolio Value)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.obs_size,),
            dtype=np.float32
        )
        
        # Action: Sell (0), Hold (1), Buy (2)
        self.action_space = spaces.Discrete(3)
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Calculate Relative Strength Index."""
        if len(prices) < period + 1:
            return 50.0  # Neutral default
        
        deltas = np.diff(prices[-period-1:])
        seed = deltas[:period]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else (100 if up > 0 else 0)
        rsi = 100.0 - 100.0 / (1.0 + rs)
        return float(rsi)
    
    def _calculate_macd(self, prices: np.ndarray) -> float:
        """Calculate MACD histogram component."""
        if len(prices) < self._macd_slow + 1:
            return 0.0
        
        # Exponential Moving Averages
        ema_12 = self._ema(prices, self._macd_fast)
        ema_26 = self._ema(prices, self._macd_slow)
        macd_line = ema_12 - ema_26
        
        # Signal line (EMA of MACD)
        macd_history = self._ema(prices, self._macd_signal)
        
        return float(macd_line - macd_history) if macd_history != 0 else 0.0
    
    def _ema(self, prices: np.ndarray, period: int) -> float:
        """Calculate Exponential Moving Average."""
        if len(prices) < period:
            return float(np.mean(prices))
        
        multiplier = 2.0 / (period + 1)
        ema = float(np.mean(prices[-period:]))
        
        for price in prices[-period:]:
            ema = price * multiplier + ema * (1 - multiplier)
        
        return ema
    
    def _calculate_volume_indicator(self, step: int) -> float:
        """
        Simplified volume indicator (price change magnitude as proxy).
        In real implementation, would use actual volume data.
        """
        if step < self._volume_period:
            return 0.5
        
        price_change = abs(self.price_data[step] - self.price_data[step - self._volume_period])
        avg_price = np.mean(self.price_data[max(0, step - self._volume_period):step])
        
        return float(np.clip(price_change / avg_price, 0.0, 1.0))
    
    def _get_observation(self) -> np.ndarray:
        """Build observation vector from current state."""
        # Get price window
        start_idx = max(0, self.current_step - self.window_size)
        end_idx = self.current_step + 1
        window = self.price_data[start_idx:end_idx]
        
        # Normalize prices to [0, 1]
        min_price = np.min(window)
        max_price = np.max(window)
        if max_price > min_price:
            normalized_prices = (window - min_price) / (max_price - min_price)
        else:
            normalized_prices = np.full_like(window, 0.5)
        
        # Pad to window size if necessary
        if len(normalized_prices) < self.window_size:
            padding = np.full(self.window_size - len(normalized_prices), 0.5)
            normalized_prices = np.concatenate([padding, normalized_prices])
        
        # Calculate technical indicators
        rsi = self._calculate_rsi(window) / 100.0  # Normalize to [0, 1]
        macd = np.clip(self._calculate_macd(window), -1, 1) * 0.5 + 0.5  # Normalize to [0, 1]
        volume = self._calculate_volume_indicator(self.current_step)
        
        # Portfolio metrics normalized
        portfolio_value = self.balance + (self.position * self.price_data[self.current_step])
        portfolio_return = (portfolio_value - self.initial_balance) / self.initial_balance
        portfolio_return = np.clip(portfolio_return, -1.0, 1.0) * 0.5 + 0.5
        
        # Concatenate all features
        observation = np.concatenate([
            normalized_prices,
            [rsi, macd, volume, portfolio_return]
        ]).astype(np.float32)
        
        return observation[:self.obs_size]  # Ensure correct size
    
    def _calculate_reward(self) -> Tuple[float, float]:
        """
        Calculate reward based on Log Returns of portfolio.
        Also returns confidence score (saliency).
        
        Returns:
            Tuple of (reward, confidence_score)
        """
        current_portfolio_value = self.balance + (self.position * self.price_data[self.current_step])
        
        # Log returns of portfolio
        if self.initial_balance > 0:
            log_return = np.log(current_portfolio_value / self.initial_balance)
        else:
            log_return = 0.0
        
        # Reward: encourage profit, penalize loss
        reward = float(log_return * 100)  # Scale for better learning
        
        # Penalize if position is losing
        if self.position > 0 and self.entry_price > self.price_data[self.current_step]:
            reward -= 0.5  # Small penalty for underwater position
        elif self.position < 0 and self.entry_price < self.price_data[self.current_step]:
            reward -= 0.5
        
        # Penalize excessive trading
        if self.last_action != 1:  # Not holding
            reward -= 0.1
        
        # Confidence score based on indicator alignment
        window = self.price_data[max(0, self.current_step - self.window_size):self.current_step + 1]
        rsi = self._calculate_rsi(window) / 100.0
        macd = np.clip(self._calculate_macd(window), -1, 1) * 0.5 + 0.5
        
        # Confidence: how aligned are the indicators?
        rsi_bullish = 1.0 if rsi > 0.7 else (0.0 if rsi < 0.3 else 0.5)
        macd_bullish = 1.0 if macd > 0.6 else (0.0 if macd < 0.4 else 0.5)
        
        if self.last_action == 2:  # Buy signal
            confidence = (rsi_bullish + macd_bullish) / 2.0
        elif self.last_action == 0:  # Sell signal
            confidence = (2.0 - rsi_bullish - macd_bullish) / 2.0
        else:  # Hold
            confidence = 0.5
        
        confidence = np.clip(float(confidence), 0.0, 1.0)
        
        return reward, confidence
    
    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, Dict]:
        """
        Reset environment to initial state.
        
        Args:
            seed: Random seed
            options: Optional configuration dict
            
        Returns:
            Tuple of (observation, info)
        """
        super().reset(seed=seed)
        
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.position = 0.0
        self.entry_price = 0.0
        self.trades = []
        self.episode_reward = 0.0
        self.last_action = 1
        
        observation = self._get_observation()
        info = {
            "balance": self.balance,
            "position": self.position,
            "price": float(self.price_data[self.current_step])
        }
        
        return observation, info
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """
        Execute one step of the environment with the given action.
        
        Args:
            action: Action to take (0: Sell, 1: Hold, 2: Buy)
            
        Returns:
            Tuple of (observation, reward, terminated, truncated, info)
        """
        self.last_action = action
        current_price = self.price_data[self.current_step]
        
        # Execute action
        if action == 2:  # Buy
            if self.balance > 0:
                units_to_buy = self.balance / current_price * (1 - self.transaction_cost)
                self.position += units_to_buy
                self.entry_price = current_price
                self.balance = 0
                self.trades.append({
                    "step": self.current_step,
                    "action": "BUY",
                    "price": current_price,
                    "units": units_to_buy
                })
        
        elif action == 0:  # Sell
            if self.position > 0:
                proceeds = self.position * current_price * (1 - self.transaction_cost)
                self.balance += proceeds
                self.position = 0
                self.trades.append({
                    "step": self.current_step,
                    "action": "SELL",
                    "price": current_price,
                    "units": 0
                })
        
        # Calculate reward and confidence
        reward, confidence = self._calculate_reward()
        self.episode_reward += reward
        
        # Move to next step
        self.current_step += 1
        terminated = self.current_step >= len(self.price_data) - 1
        truncated = self.current_step >= (self.window_size + self.max_steps)
        
        observation = self._get_observation() if not terminated else np.zeros(self.obs_size, dtype=np.float32)
        
        info = {
            "balance": self.balance,
            "position": self.position,
            "price": float(current_price),
            "reward": reward,
            "agent_confidence": confidence,
            "portfolio_value": self.balance + (self.position * current_price),
            "trades": len(self.trades),
            "episode_return": self.episode_reward
        }
        
        return observation, reward, terminated, truncated, info
    
    def get_portfolio_value(self) -> float:
        """Get current total portfolio value."""
        return self.balance + (self.position * self.price_data[self.current_step])
    
    def close(self) -> None:
        """Cleanup."""
        pass

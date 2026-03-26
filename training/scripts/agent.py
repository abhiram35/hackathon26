"""
RL Trading Agent - Main Agent Definition and Training Module
Implements the Reinforcement Learning agent for autonomous trading
"""

import os
import numpy as np
import torch
import torch.nn as nn
from datetime import datetime
from pathlib import Path
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
from gymnasium.wrappers import TimeLimit
import sys

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from environment import TradingEnv
from config import Config
from data_utils import load_price_data, generate_synthetic_prices


class TradingCallback(BaseCallback):
    """
    Custom callback for training monitoring and logging
    Tracks metrics during training and saves checkpoints
    """
    
    def __init__(self, verbose=0):
        super(TradingCallback, self).__init__(verbose)
        self.episode_rewards = []
        self.episode_lengths = []
        
    def _on_step(self) -> bool:
        """Called after every step of the environment"""
        return True
    
    def _on_training_end(self) -> None:
        """Called at the end of training"""
        print(f"\n✅ Training completed!")
        print(f"Total timesteps: {self.num_timesteps}")


class RLTradingAgent:
    """
    Main RL Trading Agent class
    Handles model creation, training, evaluation, and inference
    """
    
    def __init__(
        self,
        config: Config = None,
        model_type: str = "PPO",
        device: str = "auto",
        verbose: int = 1,
    ):
        """
        Initialize the RL Trading Agent
        
        Args:
            config: Configuration object (default: Config())
            model_type: Type of RL algorithm ("PPO", "DQN", "A2C")
            device: Device for training ("cpu", "cuda", "auto")
            verbose: Verbosity level (0=silent, 1=info, 2=debug)
        """
        self.config = config or Config()
        self.model_type = model_type
        self.device = device
        self.verbose = verbose
        
        # Model components
        self.env = None
        self.model = None
        self.callback = None
        
        # Training state
        self.training_history = {
            'rewards': [],
            'losses': [],
            'win_rates': [],
        }
        
        # Paths
        self.model_dir = Path(__file__).parent.parent / "models"
        self.log_dir = Path(__file__).parent.parent / "logs"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🤖 Initialized {model_type} Trading Agent")
        print(f"   Device: {device}")
        print(f"   Model dir: {self.model_dir}")
        
    def create_environment(self, prices: np.ndarray = None, config_preset: str = "balanced"):
        """
        Create the trading environment
        
        Args:
            prices: Price data (OHLCV). If None, generates synthetic data
            config_preset: Configuration preset ("conservative", "balanced", "aggressive")
        
        Returns:
            Created environment
        """
        # Load or generate price data
        if prices is None:
            if self.verbose > 0:
                print(f"📊 Generating synthetic price data...")
            prices = generate_synthetic_prices(n_days=252, initial_price=100)
        
        # Create environment with preset config
        if self.verbose > 0:
            print(f"🏗️  Creating trading environment ({config_preset} preset)...")
        
        self.env = TradingEnv(
            prices=prices,
            initial_balance=self.config.initial_balance,
            transaction_cost=self.config.transaction_cost,
            config_preset=config_preset,
        )
        
        # Wrap with time limit (1 episode = 1 trading day)
        self.env = TimeLimit(self.env, max_episode_steps=len(prices)-1)
        
        if self.verbose > 0:
            print(f"✅ Environment created")
            print(f"   Observation space: {self.env.observation_space}")
            print(f"   Action space: {self.env.action_space}")
        
        return self.env
    
    def create_model(self, learning_rate: float = 3e-4, policy: str = "MlpPolicy"):
        """
        Create the RL model
        
        Args:
            learning_rate: Learning rate for the optimizer
            policy: Policy network type ("MlpPolicy", "CnnPolicy")
        
        Returns:
            Created RL model
        """
        if self.env is None:
            raise RuntimeError("Environment not created. Call create_environment() first.")
        
        if self.verbose > 0:
            print(f"🧠 Creating {self.model_type} model...")
        
        # Model-specific parameters
        model_params = {
            "env": self.env,
            "policy": policy,
            "learning_rate": learning_rate,
            "verbose": self.verbose,
            "device": self.device,
            "tensorboard_log": str(self.log_dir),
        }
        
        # Create appropriate model type
        if self.model_type == "PPO":
            # PPO-specific parameters
            model_params.update({
                "n_steps": 2048,
                "batch_size": 64,
                "n_epochs": 10,
                "gamma": 0.99,
                "gae_lambda": 0.95,
                "clip_range": 0.2,
                "ent_coef": 0.01,
            })
            self.model = PPO(**model_params)
        
        elif self.model_type == "DQN":
            # DQN-specific parameters
            model_params.update({
                "learning_starts": 1000,
                "buffer_size": 10000,
                "gamma": 0.99,
                "exploration_fraction": 0.1,
                "exploration_initial_eps": 1.0,
                "exploration_final_eps": 0.05,
            })
            self.model = DQN(**model_params)
        
        elif self.model_type == "A2C":
            # A2C-specific parameters
            model_params.update({
                "n_steps": 5,
                "gamma": 0.99,
                "gae_lambda": 0.95,
                "ent_coef": 0.01,
            })
            self.model = A2C(**model_params)
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        if self.verbose > 0:
            print(f"✅ Model created with {self.model.num_parameters()} parameters")
        
        return self.model
    
    def train(
        self,
        total_timesteps: int = 100000,
        checkpoint_interval: int = 10000,
        callback_verbose: int = 1,
    ):
        """
        Train the RL agent
        
        Args:
            total_timesteps: Total timesteps to train
            checkpoint_interval: Save checkpoint every N timesteps
            callback_verbose: Callback verbosity
        
        Returns:
            Training history
        """
        if self.model is None:
            raise RuntimeError("Model not created. Call create_model() first.")
        
        if self.verbose > 0:
            print(f"\n🚀 Starting training...")
            print(f"   Total timesteps: {total_timesteps:,}")
            print(f"   Algorithm: {self.model_type}")
            print(f"   Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create callbacks
        checkpoint_callback = CheckpointCallback(
            save_freq=checkpoint_interval,
            save_path=str(self.model_dir),
            name_prefix="agent",
            verbose=callback_verbose,
        )
        
        self.callback = TradingCallback(verbose=callback_verbose)
        
        # Train the model
        try:
            self.model.learn(
                total_timesteps=total_timesteps,
                callback=[checkpoint_callback, self.callback],
                log_interval=100,
            )
            
            if self.verbose > 0:
                print(f"\n✅ Training completed successfully!")
                print(f"   End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        except KeyboardInterrupt:
            print("\n⚠️  Training interrupted by user")
        except Exception as e:
            print(f"\n❌ Training failed: {e}")
            raise
        
        return self.training_history
    
    def save_model(self, name: str = None):
        """
        Save the trained model
        
        Args:
            name: Model name (default: agent_{timestamp})
        
        Returns:
            Path to saved model
        """
        if self.model is None:
            raise RuntimeError("No model to save. Train a model first.")
        
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"agent_{self.model_type}_{timestamp}"
        
        model_path = self.model_dir / f"{name}.zip"
        
        self.model.save(str(model_path))
        
        if self.verbose > 0:
            print(f"💾 Model saved: {model_path}")
        
        return model_path
    
    def load_model(self, model_path: str):
        """
        Load a trained model
        
        Args:
            model_path: Path to model file
        
        Returns:
            Loaded model
        """
        if self.env is None:
            raise RuntimeError("Environment not created. Call create_environment() first.")
        
        # Import appropriate model class
        model_classes = {
            "PPO": PPO,
            "DQN": DQN,
            "A2C": A2C,
        }
        
        ModelClass = model_classes[self.model_type]
        self.model = ModelClass.load(model_path, env=self.env)
        
        if self.verbose > 0:
            print(f"📂 Model loaded: {model_path}")
        
        return self.model
    
    def evaluate(self, n_episodes: int = 10, render: bool = False):
        """
        Evaluate the trained agent
        
        Args:
            n_episodes: Number of episodes to evaluate
            render: Whether to render the environment
        
        Returns:
            Evaluation metrics
        """
        if self.model is None or self.env is None:
            raise RuntimeError("Model or environment not initialized.")
        
        if self.verbose > 0:
            print(f"\n📊 Evaluating agent ({n_episodes} episodes)...")
        
        episode_rewards = []
        episode_lengths = []
        
        for episode in range(n_episodes):
            obs, _ = self.env.reset()
            done = False
            total_reward = 0
            steps = 0
            
            while not done:
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                total_reward += reward
                steps += 1
                
                if render:
                    self.env.render()
            
            episode_rewards.append(total_reward)
            episode_lengths.append(steps)
            
            if self.verbose > 1:
                print(f"  Episode {episode+1}: Reward={total_reward:.2f}, Steps={steps}")
        
        # Calculate metrics
        metrics = {
            "mean_reward": np.mean(episode_rewards),
            "std_reward": np.std(episode_rewards),
            "mean_length": np.mean(episode_lengths),
            "max_reward": np.max(episode_rewards),
            "min_reward": np.min(episode_rewards),
        }
        
        if self.verbose > 0:
            print(f"\n📈 Evaluation Results:")
            print(f"   Mean reward: {metrics['mean_reward']:.2f} ± {metrics['std_reward']:.2f}")
            print(f"   Mean episode length: {metrics['mean_length']:.0f} steps")
            print(f"   Reward range: [{metrics['min_reward']:.2f}, {metrics['max_reward']:.2f}]")
        
        return metrics
    
    def predict(self, obs: np.ndarray, deterministic: bool = True):
        """
        Predict action for given observation
        
        Args:
            obs: Current observation
            deterministic: Whether to use deterministic policy
        
        Returns:
            Predicted action and prediction info
        """
        if self.model is None:
            raise RuntimeError("Model not initialized.")
        
        action, _states = self.model.predict(obs, deterministic=deterministic)
        return action
    
    def reset(self):
        """Reset the environment"""
        if self.env is not None:
            return self.env.reset()
        return None
    
    def close(self):
        """Close the environment"""
        if self.env is not None:
            self.env.close()
        if self.verbose > 0:
            print("✅ Agent closed")


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = RLTradingAgent(
        model_type="PPO",
        device="cpu",
        verbose=2,
    )
    
    # Create environment with synthetic data
    agent.create_environment(config_preset="balanced")
    
    # Create model
    agent.create_model(learning_rate=3e-4)
    
    # Train for a few steps (quick test)
    print("\n" + "="*60)
    print("TRAINING EXAMPLE")
    print("="*60)
    agent.train(total_timesteps=10000, checkpoint_interval=5000)
    
    # Save model
    print("\n" + "="*60)
    print("MODEL SAVING")
    print("="*60)
    model_path = agent.save_model("test_agent")
    
    # Evaluate
    print("\n" + "="*60)
    print("EVALUATION")
    print("="*60)
    metrics = agent.evaluate(n_episodes=5)
    
    # Cleanup
    agent.close()
    
    print("\n✅ Agent training pipeline complete!")

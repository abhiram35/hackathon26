"""
Advanced Agent Training Scenarios
Examples and templates for different training configurations
"""

from agent import RLTradingAgent
from config import Config
from data_utils import load_price_data, generate_synthetic_prices
import numpy as np
from pathlib import Path


# ============================================================================
# SCENARIO 1: Quick Training with Default Settings
# ============================================================================

def train_default_agent():
    """
    Train an agent with default settings
    Good for quick prototyping and testing
    """
    print("\n" + "="*70)
    print("SCENARIO 1: Default Agent Training")
    print("="*70)
    
    # Create agent
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    
    # Setup environment and model
    agent.create_environment(config_preset="balanced")
    agent.create_model(learning_rate=3e-4)
    
    # Train
    agent.train(total_timesteps=50000, checkpoint_interval=10000)
    
    # Evaluate
    metrics = agent.evaluate(n_episodes=10)
    
    # Save
    model_path = agent.save_model("default_ppo_agent")
    agent.close()
    
    return agent, metrics


# ============================================================================
# SCENARIO 2: Conservative Training (Low Risk)
# ============================================================================

def train_conservative_agent():
    """
    Train a conservative agent with lower risk tolerance
    Good for capital preservation strategies
    """
    print("\n" + "="*70)
    print("SCENARIO 2: Conservative Agent Training")
    print("="*70)
    
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    agent.create_environment(config_preset="conservative")
    agent.create_model(learning_rate=1e-4)  # Lower learning rate
    
    # Train with conservative parameters
    agent.train(
        total_timesteps=100000,
        checkpoint_interval=20000,
    )
    
    metrics = agent.evaluate(n_episodes=5)
    model_path = agent.save_model("conservative_agent")
    agent.close()
    
    return agent, metrics


# ============================================================================
# SCENARIO 3: Aggressive Training (High Risk/Reward)
# ============================================================================

def train_aggressive_agent():
    """
    Train an aggressive agent with higher risk tolerance
    Good for growth-focused strategies
    """
    print("\n" + "="*70)
    print("SCENARIO 3: Aggressive Agent Training")
    print("="*70)
    
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    agent.create_environment(config_preset="aggressive")
    agent.create_model(learning_rate=5e-4)  # Higher learning rate
    
    agent.train(
        total_timesteps=150000,
        checkpoint_interval=30000,
    )
    
    metrics = agent.evaluate(n_episodes=5)
    model_path = agent.save_model("aggressive_agent")
    agent.close()
    
    return agent, metrics


# ============================================================================
# SCENARIO 4: Multi-Algorithm Comparison
# ============================================================================

def compare_algorithms():
    """
    Train and compare different RL algorithms
    Useful for finding the best approach
    """
    print("\n" + "="*70)
    print("SCENARIO 4: Algorithm Comparison")
    print("="*70)
    
    algorithms = ["PPO", "DQN", "A2C"]
    results = {}
    
    for algo in algorithms:
        print(f"\n🔄 Training {algo}...")
        
        agent = RLTradingAgent(model_type=algo, verbose=0)
        agent.create_environment(config_preset="balanced")
        agent.create_model(learning_rate=3e-4)
        
        # Train
        agent.train(total_timesteps=50000, checkpoint_interval=25000)
        
        # Evaluate
        metrics = agent.evaluate(n_episodes=5)
        results[algo] = metrics
        
        # Save
        agent.save_model(f"comparison_{algo.lower()}_agent")
        agent.close()
        
        print(f"✅ {algo} completed - Mean reward: {metrics['mean_reward']:.2f}")
    
    # Compare results
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    
    for algo, metrics in results.items():
        print(f"\n{algo}:")
        print(f"  Mean Reward: {metrics['mean_reward']:.2f}")
        print(f"  Std Reward:  {metrics['std_reward']:.2f}")
        print(f"  Max Reward:  {metrics['max_reward']:.2f}")
    
    return results


# ============================================================================
# SCENARIO 5: Fine-tuning and Transfer Learning
# ============================================================================

def finetune_agent(base_model_path: str):
    """
    Fine-tune a pre-trained agent on new data
    Good for adapting to changing market conditions
    
    Args:
        base_model_path: Path to the base model to fine-tune
    """
    print("\n" + "="*70)
    print("SCENARIO 5: Agent Fine-tuning")
    print("="*70)
    
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    agent.create_environment(config_preset="balanced")
    
    # Load pre-trained model
    print(f"\n📂 Loading base model: {base_model_path}")
    agent.load_model(base_model_path)
    
    # Fine-tune with lower learning rate
    print("\n🔄 Fine-tuning on new data...")
    agent.model.learning_rate = 1e-4  # Lower learning rate for fine-tuning
    agent.train(total_timesteps=25000, checkpoint_interval=5000)
    
    # Evaluate
    metrics = agent.evaluate(n_episodes=5)
    
    # Save
    model_path = agent.save_model("finetuned_agent")
    agent.close()
    
    return agent, metrics


# ============================================================================
# SCENARIO 6: Real Market Data Training
# ============================================================================

def train_on_real_data(price_csv_path: str):
    """
    Train agent on real historical market data
    
    Args:
        price_csv_path: Path to CSV file with OHLCV data
    """
    print("\n" + "="*70)
    print("SCENARIO 6: Real Market Data Training")
    print("="*70)
    
    # Load real data
    print(f"\n📊 Loading real market data from {price_csv_path}")
    prices = load_price_data(price_csv_path)
    
    print(f"   Data shape: {prices.shape}")
    print(f"   Date range: {len(prices)} trading days")
    
    # Create agent
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    agent.create_environment(prices=prices, config_preset="balanced")
    agent.create_model(learning_rate=3e-4)
    
    # Train
    agent.train(total_timesteps=100000, checkpoint_interval=25000)
    
    # Evaluate
    metrics = agent.evaluate(n_episodes=10)
    
    # Save
    model_path = agent.save_model("realdata_agent")
    agent.close()
    
    return agent, metrics


# ============================================================================
# SCENARIO 7: Hyperparameter Tuning
# ============================================================================

def tune_hyperparameters():
    """
    Test different hyperparameter combinations
    Useful for optimizing agent performance
    """
    print("\n" + "="*70)
    print("SCENARIO 7: Hyperparameter Tuning")
    print("="*70)
    
    learning_rates = [1e-5, 1e-4, 3e-4, 1e-3]
    results = {}
    
    for lr in learning_rates:
        print(f"\n🔧 Testing learning rate: {lr}")
        
        agent = RLTradingAgent(model_type="PPO", verbose=0)
        agent.create_environment(config_preset="balanced")
        agent.create_model(learning_rate=lr)
        
        agent.train(total_timesteps=50000, checkpoint_interval=25000)
        metrics = agent.evaluate(n_episodes=5)
        
        results[lr] = metrics['mean_reward']
        
        print(f"   Mean Reward: {metrics['mean_reward']:.2f}")
        
        agent.close()
    
    # Find best learning rate
    best_lr = max(results, key=results.get)
    print(f"\n✅ Best learning rate: {best_lr}")
    print(f"   Mean Reward: {results[best_lr]:.2f}")
    
    return results


# ============================================================================
# SCENARIO 8: Continuous Training (Online Learning)
# ============================================================================

def train_continuously(episodes: int = 10, steps_per_episode: int = 10000):
    """
    Train agent continuously with periodic saves
    Good for long-term adaptation
    
    Args:
        episodes: Number of training episodes
        steps_per_episode: Steps per episode
    """
    print("\n" + "="*70)
    print("SCENARIO 8: Continuous Training")
    print("="*70)
    
    agent = RLTradingAgent(model_type="PPO", verbose=1)
    agent.create_environment(config_preset="balanced")
    agent.create_model(learning_rate=3e-4)
    
    total_steps = 0
    
    for episode in range(episodes):
        print(f"\n--- Training Episode {episode+1}/{episodes} ---")
        
        # Train for N steps
        agent.train(
            total_timesteps=steps_per_episode,
            checkpoint_interval=steps_per_episode,
        )
        
        total_steps += steps_per_episode
        
        # Evaluate periodically
        if (episode + 1) % 3 == 0:
            print(f"\n📊 Periodic Evaluation (Episode {episode+1})")
            metrics = agent.evaluate(n_episodes=3)
            print(f"   Mean reward: {metrics['mean_reward']:.2f}")
        
        # Save checkpoint
        agent.save_model(f"continuous_agent_episode_{episode+1}")
    
    agent.close()
    print(f"\n✅ Continuous training completed ({total_steps} total steps)")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main entry point with scenario selection"""
    
    print("\n" + "="*70)
    print("RL TRADING AGENT - TRAINING SCENARIOS")
    print("="*70)
    print("\nSelect a training scenario:")
    print("  1. Default Agent Training (PPO, 50k steps)")
    print("  2. Conservative Agent (Low Risk)")
    print("  3. Aggressive Agent (High Risk)")
    print("  4. Compare Algorithms (PPO vs DQN vs A2C)")
    print("  5. Fine-tune Pre-trained Agent")
    print("  6. Train on Real Market Data")
    print("  7. Hyperparameter Tuning")
    print("  8. Continuous Training (Online Learning)")
    print("  0. Exit")
    
    choice = input("\nEnter scenario number (0-8): ").strip()
    
    try:
        if choice == "1":
            train_default_agent()
        elif choice == "2":
            train_conservative_agent()
        elif choice == "3":
            train_aggressive_agent()
        elif choice == "4":
            compare_algorithms()
        elif choice == "5":
            # Use most recent model if available
            model_dir = Path(__file__).parent.parent / "models"
            model_files = list(model_dir.glob("*.zip"))
            if model_files:
                latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
                finetune_agent(str(latest_model))
            else:
                print("❌ No pre-trained models found. Train one first.")
        elif choice == "6":
            csv_path = input("Enter path to CSV file: ").strip()
            train_on_real_data(csv_path)
        elif choice == "7":
            tune_hyperparameters()
        elif choice == "8":
            episodes = int(input("Number of continuous episodes (default 10): ") or "10")
            train_continuously(episodes=episodes)
        elif choice == "0":
            print("👋 Exiting...")
        else:
            print("❌ Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

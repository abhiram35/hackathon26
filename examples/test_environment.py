"""Quick test of environment functionality"""
import numpy as np
from environment import TradingEnv

print("\n" + "="*70)
print("ENVIRONMENT FUNCTIONALITY TEST")
print("="*70 + "\n")

# Generate test price data
prices = np.array([100.0, 101.5, 99.8, 102.3, 100.5, 103.0, 102.2, 
                   105.5, 104.0, 106.2, 105.8, 107.5, 106.8, 109.0,
                   108.5, 110.2, 109.5, 112.0, 111.5, 113.2, 112.8,
                   115.0, 114.5, 117.0, 116.5, 119.0, 118.5, 121.0], dtype=np.float32)

try:
    # Initialize environment
    env = TradingEnv(
        price_data=prices,
        initial_balance=10000.0,
        window_size=5,
        transaction_cost=0.001
    )
    print("✅ Environment initialized successfully")
    print(f"   Initial balance: ${env.initial_balance:,.2f}")
    print(f"   Price data length: {len(prices)}")
    print(f"   Observation space: {env.observation_space}")
    print(f"   Action space: {env.action_space}")
    
    # Test reset
    obs, info = env.reset()
    print(f"\n✅ Reset successful")
    print(f"   Observation shape: {obs.shape}")
    print(f"   Observation range: [{obs.min():.3f}, {obs.max():.3f}]")
    print(f"   Starting price: ${info['price']:.2f}")
    print(f"   Starting balance: ${info['balance']:.2f}")
    
    # Test step
    action = 2  # BUY
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"\n✅ Step executed (action: BUY)")
    print(f"   Reward: {reward:.4f}")
    print(f"   Position: {env.position:.2f} units")
    print(f"   Balance: ${env.balance:.2f}")
    print(f"   Agent confidence: {info['agent_confidence']:.2%}")
    print(f"   Episode return: {info['episode_return']:.4f}")
    
    # Test multiple steps
    for i in range(3):
        action = np.random.randint(0, 3)
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break
    
    print(f"\n✅ Multiple steps executed")
    print(f"   Portfolio value: ${info['portfolio_value']:.2f}")
    print(f"   Total trades: {len(env.trades)}")
    print(f"   Episode reward accumulated: {env.episode_reward:.4f}")
    
    # Test technical indicators
    print(f"\n✅ Technical indicators calculated")
    print(f"   RSI (last): {env._calculate_rsi(prices[max(0, env.current_step-14):env.current_step+1])/100:.2%}")
    print(f"   MACD (last): {env._calculate_macd(prices[max(0, env.current_step-26):env.current_step+1]):.4f}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - Environment functional!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

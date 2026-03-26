"""
Quick-start example for the RL Trading Agent.
Run this after starting the FastAPI server to test the system.

Usage:
    1. Start MongoDB and FastAPI server
    2. python example.py
"""

import requests
import json
import time
import numpy as np
from datetime import datetime

API_URL = "http://localhost:8000"


def generate_synthetic_prices(length: int = 500, start_price: float = 100.0) -> list:
    """Generate realistic synthetic stock prices using geometric brownian motion."""
    returns = np.random.normal(0.0005, 0.02, length)
    prices = start_price * np.exp(np.cumsum(returns))
    return prices.tolist()


def print_header(text: str) -> None:
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def test_health() -> bool:
    """Test API health and database connection."""
    print_header("1. Testing API Health")
    
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ API Status: {data['status']}")
        print(f"✅ Database: {data['database']}")
        print(f"✅ Timestamp: {data['timestamp']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("  1. MongoDB is running")
        print("  2. FastAPI server is running: uvicorn main:app --reload")
        print("  3. MONGODB_URI environment variable is set (or using default localhost)")
        return False


def test_training() -> str:
    """Start a training session."""
    print_header("2. Starting Training Session")
    
    # Generate synthetic price data
    print("📊 Generating synthetic price data...")
    prices = generate_synthetic_prices(length=500, start_price=100.0)
    print(f"   Generated {len(prices)} price points")
    print(f"   Price range: ${min(prices):.2f} - ${max(prices):.2f}")
    
    # Prepare request
    request_data = {
        "episodes": 100,
        "total_timesteps": 5000,
        "price_data": prices,
        "initial_balance": 10000.0,
        "session_name": "QuickStart_Example"
    }
    
    print("\n🔥 Submitting training request...")
    try:
        response = requests.post(
            f"{API_URL}/train",
            json=request_data,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        session_id = data["session_id"]
        
        print(f"✅ Training session created!")
        print(f"   Session ID: {session_id}")
        print(f"   Status: {data['status']}")
        print(f"   Message: {data['message']}")
        
        return session_id
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def monitor_training(session_id: str, max_wait: int = 120) -> dict:
    """Monitor training progress."""
    print_header("3. Monitoring Training Progress")
    
    print(f"⏳ Waiting for training to complete (max {max_wait}s)...")
    print("   Checking every 10 seconds...\n")
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{API_URL}/replay/{session_id}")
            response.raise_for_status()
            
            data = response.json()
            status = data["status"]
            
            if status != last_status:
                elapsed = int(time.time() - start_time)
                print(f"   [{elapsed}s] Status: {status.upper()}")
                last_status = status
            
            if status == "completed":
                print(f"\n✅ Training completed!")
                return data
            elif status == "failed":
                print(f"\n❌ Training failed!")
                return data
            
            time.sleep(10)
        except Exception as e:
            print(f"⚠️  Error checking status: {e}")
            time.sleep(10)
    
    print(f"\n⏱️  Timeout reached after {max_wait}s")
    print("   Note: Training may still be running in background")
    print("   Check status later with: GET /replay/{session_id}")
    
    return None


def analyze_results(session_data: dict) -> None:
    """Analyze and display training results."""
    print_header("4. Analyzing Results")
    
    if not session_data:
        print("❌ No session data available")
        return
    
    print(f"Session ID: {session_data['session_id']}")
    print(f"Status: {session_data['status']}")
    print(f"Created: {session_data['created_at']}")
    
    if session_data.get("completed_at"):
        print(f"Completed: {session_data['completed_at']}")
    
    print("\n💰 Financial Metrics:")
    print(f"   Initial Balance: ${session_data['initial_balance']:,.2f}")
    print(f"   Final Balance: ${session_data['final_balance']:,.2f}")
    print(f"   Total Return: {session_data['total_return']*100:+.2f}%")
    
    print(f"\n📊 Trading Metrics:")
    print(f"   Steps Taken: {session_data['num_steps']}")
    
    # Analyze agent confidence
    steps = session_data.get("steps", [])
    if steps:
        confidences = [s["agent_confidence"] for s in steps]
        actions = [s["action"] for s in steps]
        rewards = [s["reward"] for s in steps]
        
        action_names = {0: "SELL", 1: "HOLD", 2: "BUY"}
        action_count = {0: 0, 1: 0, 2: 0}
        
        for action in actions:
            action_count[action] += 1
        
        print(f"\n🎯 Agent Confidence:")
        print(f"   Average: {np.mean(confidences):.2%}")
        print(f"   Max: {np.max(confidences):.2%}")
        print(f"   Min: {np.min(confidences):.2%}")
        
        print(f"\n📈 Action Distribution:")
        for action_id, name in action_names.items():
            count = action_count[action_id]
            pct = (count / len(actions) * 100) if actions else 0
            print(f"   {name}: {count} ({pct:.1f}%)")
        
        print(f"\n🏆 Top 5 High-Confidence Trades:")
        
        # Find high confidence trades
        high_conf_trades = []
        for i, step in enumerate(steps):
            if step["action"] != 1:  # Exclude holds
                high_conf_trades.append((i, step["action"], step["agent_confidence"], step["price"]))
        
        high_conf_trades.sort(key=lambda x: x[2], reverse=True)
        
        for i, (step_num, action, conf, price) in enumerate(high_conf_trades[:5], 1):
            action_name = action_names[action]
            print(f"   {i}. Step {step_num}: {action_name} @ ${price:.2f} (confidence: {conf:.2%})")
    
    print()


def test_list_sessions() -> None:
    """List all sessions."""
    print_header("5. Listing All Sessions")
    
    try:
        response = requests.get(f"{API_URL}/sessions?limit=10")
        response.raise_for_status()
        
        data = response.json()
        
        print(f"Total Sessions: {data['total_sessions']}")
        print(f"Completed: {data['completed_sessions']}")
        print(f"Average Return: {data['avg_return']*100:+.2f}%\n")
        
        if data["sessions"]:
            print("Recent Sessions:")
            print("-" * 70)
            for session in data["sessions"][:5]:
                return_pct = session["total_return"] * 100
                print(f"  {session['session_id'][:8]}... | Return: {return_pct:+.2f}% | Steps: {session['num_steps']:4d} | Status: {session['status']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  RL TRADING AGENT - QUICKSTART EXAMPLE".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Test 1: Health check
    if not test_health():
        return
    
    # Test 2: Start training
    session_id = test_training()
    if not session_id:
        return
    
    # Test 3: Monitor training
    session_data = monitor_training(session_id, max_wait=180)
    
    # Test 4: Analyze results
    if session_data:
        analyze_results(session_data)
    
    # Test 5: List sessions
    test_list_sessions()
    
    print_header("✅ Quick-Start Complete!")
    
    print("📚 Next Steps:")
    print("   1. Review the generated session data above")
    print("   2. Check README.md for detailed documentation")
    print("   3. Access interactive API docs: http://localhost:8000/docs")
    print("   4. Experiment with different price data and parameters")
    print("\n💡 Tips:")
    print("   - Use GET /replay/{session_id} to fetch sessions later")
    print("   - Check GET /sessions/{session_id}/stats for detailed analytics")
    print("   - Monitor agent_confidence scores to understand agent decisions")
    print()


if __name__ == "__main__":
    main()

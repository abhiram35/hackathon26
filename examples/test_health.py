"""Quick test of API health"""
import urllib.request
import json

try:
    response = urllib.request.urlopen('http://localhost:8000/health', timeout=5)
    data = json.loads(response.read().decode())
    print("\n" + "="*70)
    print("✅ API IS RUNNING AND HEALTHY")
    print("="*70)
    print(f"Status: {data['status']}")
    print(f"Database: {data['database']}")
    print(f"Timestamp: {data['timestamp']}")
    print("="*70 + "\n")
except Exception as e:
    print(f"❌ Error: {e}")

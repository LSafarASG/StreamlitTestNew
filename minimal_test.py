#!/usr/bin/env python3
"""
Minimal test to isolate the backend performance issue.
"""

import requests
import time
import json

def test_minimal():
    """Test with minimal overhead."""
    backend_url = "https://streamlittestnewbackend.onrender.com"
    
    print("🔍 Testing minimal backend performance...")
    print(f"📡 Backend: {backend_url}")
    print("-" * 40)
    
    # Test 1: Simple ping
    print("1️⃣ Testing simple endpoint...")
    start = time.time()
    try:
        response = requests.get(f"{backend_url}/random-test-data", timeout=5)
        end = time.time()
        print(f"   Response time: {end - start:.3f}s")
        print(f"   Status: {response.status_code}")
        print(f"   Response size: {len(response.content)} bytes")
        
        # Check if response has performance data
        try:
            data = response.json()
            if 'performance' in data:
                print(f"   Backend processing: {data['performance'].get('processing_time_ms', 'N/A')}ms")
        except:
            pass
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Check if it's a network issue
    print("2️⃣ Testing network latency...")
    start = time.time()
    try:
        response = requests.get(f"{backend_url}/docs", timeout=5)  # FastAPI docs endpoint
        end = time.time()
        print(f"   Docs response time: {end - start:.3f}s")
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Check if it's Python/import related
    print("3️⃣ Testing import overhead...")
    import_start = time.time()
    try:
        import random
        import_end = time.time()
        print(f"   Import time: {import_end - import_start:.3f}s")
    except Exception as e:
        print(f"   ❌ Import error: {e}")

if __name__ == "__main__":
    print("🚀 Minimal Backend Performance Test")
    print("=" * 50)
    test_minimal()
    print("=" * 50)
    print("💡 If response times are still 2+ seconds, the issue is:")
    print("   - Network/proxy configuration")
    print("   - Uvicorn server setup")
    print("   - System-level interference")

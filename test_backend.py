#!/usr/bin/env python3
"""
Simple script to test backend performance directly without Streamlit.
This will help identify if the bottleneck is in the backend or Streamlit.
"""

import requests
import time
import statistics

def test_backend_performance(endpoint: str, num_requests: int = 5):
    """Test backend endpoint performance with multiple requests."""
    backend_url = "http://localhost:8000"
    url = f"{backend_url}{endpoint}"
    
    print(f"🔍 Testing endpoint: {endpoint}")
    print(f"📡 Backend URL: {url}")
    print(f"🔄 Number of requests: {num_requests}")
    print("-" * 50)
    
    response_times = []
    
    for i in range(num_requests):
        print(f"Request {i+1}/{num_requests}...", end=" ")
        
        start_time = time.time()
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            end_time = time.time()
            
            response_time = end_time - start_time
            response_times.append(response_time)
            
            print(f"✅ {response_time:.3f}s")
            
            # Show response data size
            data_size = len(response.content)
            print(f"   📊 Response size: {data_size:,} bytes")
            
            # Show performance data if available
            try:
                data = response.json()
                if 'performance' in data:
                    perf = data['performance']
                    print(f"   ⏱️ Backend processing: {perf.get('processing_time_ms', 'N/A')}ms")
            except:
                pass
                
        except Exception as e:
            print(f"❌ Error: {e}")
            response_times.append(None)
    
    print("-" * 50)
    
    # Calculate statistics
    valid_times = [t for t in response_times if t is not None]
    
    if valid_times:
        print(f"📈 Performance Summary:")
        print(f"   Fastest: {min(valid_times):.3f}s")
        print(f"   Slowest: {max(valid_times):.3f}s")
        print(f"   Average: {statistics.mean(valid_times):.3f}s")
        print(f"   Median: {statistics.median(valid_times):.3f}s")
        
        if len(valid_times) > 1:
            print(f"   Std Dev: {statistics.stdev(valid_times):.3f}s")
    else:
        print("❌ No successful requests to analyze")

def test_all_endpoints():
    """Test all available endpoints."""
    endpoints = [
        "/random-test-data",
        "/random-test-data-fast", 
        "/country-allocation",
        "/sector-allocation"
    ]
    
    print("🚀 Backend Performance Test")
    print("=" * 60)
    
    for endpoint in endpoints:
        test_backend_performance(endpoint, num_requests=3)
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print("Starting backend performance test...")
    print("Make sure your backend is running on http://localhost:8000")
    print()
    
    try:
        test_all_endpoints()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Make sure your backend is running and accessible")

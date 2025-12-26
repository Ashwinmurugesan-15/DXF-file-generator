import requests
import json
import time

# Wait for server to start
time.sleep(2)

url = "http://localhost:8000/generate"

# Test case: Beam with 0 height
payload = {
    "component_type": "beam",
    "params": {
        "H": 0,
        "B": 100,
        "tw": 5,
        "tf": 8
    }
}

try:
    print(f"Sending request with H=0 to {url}...")
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    if response.status_code == 400 and "must be between 1" in response.text:
        print("SUCCESS: Validation correctly rejected the zero value.")
    else:
        print("FAILURE: Validation did not behave as expected.")

except Exception as e:
    print(f"Error: {e}")

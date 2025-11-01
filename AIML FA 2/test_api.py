#!/usr/bin/env python3
"""
Test script to verify the API works correctly with sample data
"""
import requests
import json

# Test data matching the frontend form
test_data = {
    "Gender": "Male",
    "Age": 28,
    "Occupation": "Software Engineer", 
    "Sleep Duration": 7.5,
    "Physical Activity Level": 60,
    "Stress Level": 6,
    "BMI Category": "Normal",
    "Blood Pressure": "120/80",
    "Heart Rate": 72,
    "Daily Steps": 8000,
    "Sleep Disorder": "None"
}

def test_api():
    url = "http://127.0.0.1:5000/api/predict"
    
    try:
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print(f"Prediction: {result['prediction']}")
            print("Probabilities:")
            for label, prob in result['probabilities'].items():
                print(f"  {label}: {prob*100:.1f}%")
        else:
            print(f"❌ API Test Failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running")
        print("Run: python sleepbuddy_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing SleepBuddy API...")
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    test_api()



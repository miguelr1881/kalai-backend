#!/usr/bin/env python3
"""
Script para probar endpoint de treatments directamente
"""
import requests
import json

try:
    response = requests.get('http://localhost:8000/api/public/treatments')
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"\nResponse Text:")
    print(response.text)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Found {len(data)} treatments")
    else:
        print(f"\n❌ Error {response.status_code}")
except Exception as e:
    print(f"❌ Exception: {e}")

#!/usr/bin/env python3
import requests

# Login
login_response = requests.post(
    'http://localhost:8000/api/admin/login',
    json={'username': 'admin', 'password': 'kalai2026'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"✅ Token obtenido: {token[:20]}...")
    
    # Test products endpoint
    products_response = requests.get(
        'http://localhost:8000/api/admin/products',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f"\n📦 Productos: {len(products_response.json())} - Status: {products_response.status_code}")
    
    # Test treatments endpoint
    treatments_response = requests.get(
        'http://localhost:8000/api/admin/treatments',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f"✨ Tratamientos: {len(treatments_response.json())} - Status: {treatments_response.status_code}")
    
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)

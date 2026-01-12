#!/usr/bin/env python3
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("Testing FastAPI Hello World App\n" + "="*40)

# Test root endpoint
response = client.get("/")
print(f"\nGET / => Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test name endpoint
response = client.get("/hello/Alice")
print(f"\nGET /hello/Alice => Status: {response.status_code}")
print(f"Response: {response.json()}")

response = client.get("/hello/World")
print(f"\nGET /hello/World => Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n" + "="*40)
print("FastAPI is working perfectly!")

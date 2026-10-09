import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

print("1. Testing Registration...")
reg_res = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "testuser@example.com",
    "password": "password123",
    "full_name": "Test User",
    "role": "DOCUMENT_OWNER"
})
print("Register:", reg_res.status_code, reg_res.text)

print("\n2. Testing Login...")
login_res = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "testuser@example.com",
    "password": "password123"
})
print("Login:", login_res.status_code)
if login_res.status_code != 200:
    print("FAILED LOGIN:", login_res.text)
    exit(1)

token = login_res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print("\n3. Testing Upload...")
# Create a dummy file
with open("test.pdf", "wb") as f:
    f.write(b"dummy pdf content")

with open("test.pdf", "rb") as f:
    upload_res = requests.post(f"{BASE_URL}/documents/upload", headers=headers, files={"file": ("test.pdf", f, "application/pdf")})

print("Upload:", upload_res.status_code, upload_res.text)
if upload_res.status_code != 200:
    exit(1)

doc_id = upload_res.json()["id"]

print("\n4. Testing Analyze...")
analyze_res = requests.post(f"{BASE_URL}/documents/{doc_id}/analyze", headers=headers)
print("Analyze:", analyze_res.status_code, analyze_res.text)

print("\n5. Waiting for background analysis...")
time.sleep(3)

print("\n6. Fetching Analysis Results...")
get_res = requests.get(f"{BASE_URL}/documents/{doc_id}/analysis", headers=headers)
print("Analysis Results:", get_res.status_code, get_res.text)

print("\n7. Fetching PDF Report...")
report_res = requests.get(f"{BASE_URL}/documents/{doc_id}/report", headers=headers)
print("Report Results:", report_res.status_code, report_res.text)

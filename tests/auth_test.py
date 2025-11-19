# test_auth.py
import os
from dotenv import load_dotenv
from fusionauth.fusionauth_client import FusionAuthClient

# Load environment variables
load_dotenv()

api_key = os.getenv("FUSION_AUTH_API_KEY")
base_url = os.getenv("FUSION_AUTH_BASE_URI")
username = os.getenv("LOCUST_USERNAME")
password = os.getenv("LOCUST_USER_PASSWORD")

print(f"🔐 Testing FusionAuth authentication...")
print(f"Base URL: {base_url}")
print(f"Username: {username}")
print()

try:
    # Create client
    client = FusionAuthClient(api_key, base_url)
    
    # Attempt login
    print("Attempting login...")
    response = client.login({
        "loginId": username,
        "password": password
    })
    
    if response.was_successful():
        print("✅ Authentication SUCCESSFUL!")
        token = response.success_response.get("token")
        print(f"Token (first 40 chars): {token[:40]}...")
        print(f"Token length: {len(token)} characters")
    else:
        print("❌ Authentication FAILED")
        print(f"Status: {response.status}")
        print(f"Error: {response.error_response}")
        
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check your FUSION_AUTH_BASE_URI doesn't include /api/login")
    print("2. Verify credentials are correct")
    print("3. Make sure you can access the staging environment")
"""
Complete POC Example - All Integrations

This file demonstrates a complete load test with all integrations:
- Basic HTTP testing
- GraphQL queries
- Datadog reporting
- Response validation
- Realistic user behavior

This is a reference implementation you can adapt for your specific needs.
"""

from locust import HttpUser, task, between, events
from locust.exception import RescheduleTask
import json
import random
import os
from datetime import datetime

# Import Datadog reporter if available
try:
    from utils.datadog_reporter import setup_datadog_reporting
    DATADOG_AVAILABLE = True
except ImportError:
    DATADOG_AVAILABLE = False
    print("⚠️  Datadog reporter not available")


# =============================================================================
# SETUP DATADOG INTEGRATION
# =============================================================================
# This listener sets up Datadog reporting when Locust initializes

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Initialize integrations when Locust starts."""
    if DATADOG_AVAILABLE and os.getenv('DATADOG_API_KEY'):
        print("✅ Enabling Datadog integration")
        setup_datadog_reporting(environment)
    else:
        print("ℹ️  Datadog integration not configured")


# =============================================================================
# COMPLETE USER CLASS
# =============================================================================

class RealisticWebUser(HttpUser):
    """
    A realistic user that:
    1. Authenticates on start
    2. Performs various tasks with realistic weights
    3. Validates responses
    4. Reports custom metrics
    5. Handles errors gracefully
    """
    
    # Wait time between tasks (simulates user "think time")
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Called once when the user starts.
        Perfect for authentication and setup.
        """
        print(f"🚀 User {id(self)} starting...")
        
        # Store user-specific data
        self.user_id = f"user_{random.randint(1000, 9999)}"
        self.session_start = datetime.utcnow()
        self.requests_made = 0
        
        # Authenticate (if your app requires it)
        self.authenticate()
        
        print(f"✅ User {self.user_id} ready")
    
    def authenticate(self):
        """
        Authenticate the user.
        Adapt this to your authentication method.
        """
        # Example: Basic authentication
        # username = os.getenv('TEST_USERNAME', 'test_user')
        # password = os.getenv('TEST_PASSWORD', 'test_pass')
        # 
        # response = self.client.post(
        #     "/api/login",
        #     json={"username": username, "password": password},
        #     name="Authentication"
        # )
        # 
        # if response.status_code == 200:
        #     self.auth_token = response.json().get("token")
        # else:
        #     print(f"❌ Authentication failed for {self.user_id}")
        
        # For now, we'll just simulate successful auth
        self.auth_token = "simulated_token"
    
    def get_auth_headers(self):
        """Get headers with authentication token."""
        if hasattr(self, 'auth_token') and self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}"}
        return {}
    
    # =========================================================================
    # TASKS - These define what users do
    # =========================================================================
    
    @task(5)
    def browse_homepage(self):
        """
        Most common action: Just browsing the homepage.
        Weight: 5 (happens 5x more than weight-1 tasks)
        """
        self.requests_made += 1
        
        with self.client.get(
            "/",
            headers=self.get_auth_headers(),
            name="Homepage",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                # Validate response content
                if "<!DOCTYPE html>" in response.text or "<html" in response.text:
                    response.success()
                else:
                    response.failure("Homepage didn't return HTML")
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(3)
    def search_products(self):
        """
        Search for products.
        Weight: 3 (common action)
        """
        self.requests_made += 1
        
        # Realistic search terms
        search_terms = [
            "laptop", "phone", "headphones", "keyboard", 
            "mouse", "monitor", "desk", "chair"
        ]
        query = random.choice(search_terms)
        
        with self.client.get(
            f"/api/search?q={query}",
            headers=self.get_auth_headers(),
            name="Search API",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and "results" in data:
                        result_count = len(data["results"])
                        print(f"🔍 Search '{query}' returned {result_count} results")
                        response.success()
                    else:
                        response.failure("Invalid search response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Search failed: {response.status_code}")
    
    @task(2)
    def view_product_details(self):
        """
        View a specific product.
        Weight: 2 (moderately common)
        """
        self.requests_made += 1
        
        # In real scenario, you'd pick from actual product IDs
        product_id = random.randint(1, 100)
        
        with self.client.get(
            f"/api/products/{product_id}",
            headers=self.get_auth_headers(),
            name="Product Detail API",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Validate expected fields
                    required_fields = ["id", "name", "price"]
                    missing_fields = [f for f in required_fields if f not in data]
                    
                    if missing_fields:
                        response.failure(f"Missing fields: {missing_fields}")
                    else:
                        response.success()
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 404:
                # 404s are expected for non-existent products
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(1)
    def graphql_query(self):
        """
        Make a GraphQL query.
        Weight: 1 (less common)
        
        Demonstrates GraphQL testing.
        """
        self.requests_made += 1
        
        query = """
        query GetUserProfile($userId: ID!) {
            user(id: $userId) {
                id
                name
                email
            }
        }
        """
        
        variables = {"userId": self.user_id}
        
        with self.client.post(
            "/graphql",
            json={"query": query, "variables": variables},
            headers={**self.get_auth_headers(), "Content-Type": "application/json"},
            name="GraphQL: User Profile",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check for GraphQL errors
                    if "errors" in data:
                        errors = [e.get("message", "Unknown") for e in data["errors"]]
                        response.failure(f"GraphQL errors: {errors}")
                    elif "data" in data and "user" in data["data"]:
                        response.success()
                    else:
                        response.failure("Unexpected GraphQL response structure")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"GraphQL request failed: {response.status_code}")
    
    @task(1)
    def add_to_cart(self):
        """
        Add item to cart (mutation/write operation).
        Weight: 1 (least common - conversion action)
        """
        self.requests_made += 1
        
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 3)
        
        with self.client.post(
            "/api/cart/add",
            json={
                "product_id": product_id,
                "quantity": quantity,
                "user_id": self.user_id
            },
            headers=self.get_auth_headers(),
            name="Add to Cart API",
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    if data.get("success"):
                        print(f"🛒 Added product {product_id} to cart")
                        response.success()
                    else:
                        response.failure("Add to cart reported failure")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Add to cart failed: {response.status_code}")
    
    def on_stop(self):
        """
        Called when the user stops.
        Good place for cleanup and final metrics.
        """
        duration = (datetime.utcnow() - self.session_start).total_seconds()
        print(f"👋 User {self.user_id} stopping after {duration:.1f}s "
              f"({self.requests_made} requests)")


# =============================================================================
# DIFFERENT USER TYPES
# =============================================================================
# Real applications have different types of users with different behaviors

class BrowserUser(HttpUser):
    """
    User who mostly browses, rarely converts.
    Represents window shoppers.
    """
    wait_time = between(2, 5)
    
    @task(10)
    def browse(self):
        self.client.get("/", name="Browse: Homepage")
    
    @task(5)
    def search(self):
        query = random.choice(["laptop", "phone", "tablet"])
        self.client.get(f"/api/search?q={query}", name="Browse: Search")
    
    @task(1)
    def view_product(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", name="Browse: Product")


class BuyerUser(HttpUser):
    """
    User who browses less but converts more.
    Represents motivated shoppers.
    """
    wait_time = between(1, 3)
    
    @task(3)
    def search(self):
        query = random.choice(["laptop", "phone", "tablet"])
        self.client.get(f"/api/search?q={query}", name="Buyer: Search")
    
    @task(5)
    def view_product(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", name="Buyer: Product")
    
    @task(2)
    def add_to_cart(self):
        self.client.post(
            "/api/cart/add",
            json={"product_id": random.randint(1, 100), "quantity": 1},
            name="Buyer: Add to Cart"
        )


# =============================================================================
# HOW TO USE THIS FILE
# =============================================================================
"""
1. WITH SINGLE USER TYPE (RealisticWebUser):
   locust -f tests/complete_example.py --host=https://staging.yourapp.com

2. WITH MULTIPLE USER TYPES (mix of browsers and buyers):
   locust -f tests/complete_example.py --host=https://staging.yourapp.com
   
   In the UI, you can set the ratio of different user types.
   
3. HEADLESS MODE:
   locust -f tests/complete_example.py \
     --host=https://staging.yourapp.com \
     --users 50 \
     --spawn-rate 5 \
     --run-time 2h \
     --headless

4. WITH DATADOG:
   Make sure DATADOG_API_KEY and DATADOG_APP_KEY are set in .env
   Then run normally - metrics will automatically be sent to Datadog

5. QUICK TEST:
   python locust_helper.py quick tests/complete_example.py

CUSTOMIZATION CHECKLIST:
- [ ] Update authentication method in authenticate()
- [ ] Replace endpoint URLs with your actual API endpoints
- [ ] Adjust task weights based on your traffic patterns
- [ ] Add your specific GraphQL queries
- [ ] Update response validation logic
- [ ] Configure user ratios (browsers vs buyers)
- [ ] Set appropriate wait times for your use case
"""

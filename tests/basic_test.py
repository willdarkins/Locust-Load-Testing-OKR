"""
Basic Locust Test Example

This file demonstrates the fundamental concepts of Locust load testing.
It's designed to be educational for team members new to Locust and Python.

Key Concepts Demonstrated:
- User class definition
- Task definition and weighting
- Wait times between requests
- HTTP request methods
- Response validation
"""

from locust import HttpUser, task, between
import json

# =============================================================================
# UNDERSTANDING THE HttpUser CLASS
# =============================================================================
# HttpUser is the base class for all your load test users.
# Each instance represents one virtual user (VU) executing your test scenario.
# Think of it as a robot that follows the instructions you give it.

class BasicWebsiteUser(HttpUser):
    """
    Represents a typical user interacting with our React application.
    
    Attributes:
        wait_time: Time the user waits between tasks (simulates "think time")
        host: The base URL of the application (set via command line or config)
    """
    
    # =============================================================================
    # WAIT_TIME EXPLANATION
    # =============================================================================
    # Real users don't immediately click the next button - they read, think, etc.
    # wait_time simulates this realistic behavior
    # between(1, 3) means wait randomly between 1-3 seconds after each task
    wait_time = between(1, 3)
    
    # =============================================================================
    # ON_START METHOD
    # =============================================================================
    # This method runs once when the virtual user "spawns" (starts)
    # Use it for setup tasks like authentication, loading initial data, etc.
    def on_start(self):
        """
        Called once per user when they start.
        Perfect for login, getting auth tokens, etc.
        """
        # Example: You might authenticate here
        # response = self.client.post("/api/login", json={
        #     "username": "test_user",
        #     "password": "test_pass"
        # })
        # self.auth_token = response.json()["token"]
        
        print(f"User started - ready to run tasks")
    
    # =============================================================================
    # TASK DEFINITION
    # =============================================================================
    # Tasks are the actions your virtual users perform
    # The @task decorator marks a method as something the user can do
    # The number in @task(3) is the weight - higher numbers = more frequent
    
    @task(3)  # Weight of 3 - this task is 3x more likely than weight-1 tasks
    def view_homepage(self):
        """
        Simulates a user viewing the homepage.
        
        Task Weight: 3 (most common action)
        Expected: Fast response, should be cached
        """
        # self.client is an HTTP client (like requests library)
        # It automatically prepends the host URL
        # name parameter groups similar requests in reports
        response = self.client.get(
            "/",
            name="Homepage"  # This name appears in Locust UI/reports
        )
        
        # =============================================================================
        # RESPONSE VALIDATION
        # =============================================================================
        # Always validate responses to catch errors during load testing
        # If validation fails, Locust marks it as a failure in reports
        if response.status_code != 200:
            print(f"Homepage failed with status: {response.status_code}")
        
        # Optional: Validate response content
        if "<!DOCTYPE html>" not in response.text:
            response.failure("Homepage didn't return HTML")
    
    @task(2)  # Weight of 2 - moderately common
    def view_product_list(self):
        """
        Simulates browsing a product listing page.
        
        Task Weight: 2
        Expected: Should return JSON with product data
        """
        response = self.client.get(
            "/api/products",
            name="Product List API"
        )
        
        if response.status_code == 200:
            try:
                # Validate JSON response structure
                data = response.json()
                if "products" not in data:
                    response.failure("Missing 'products' key in response")
            except json.JSONDecodeError:
                response.failure("Response was not valid JSON")
        else:
            print(f"Product list failed: {response.status_code}")
    
    @task(1)  # Weight of 1 - least common action
    def view_product_detail(self):
        """
        Simulates viewing a specific product detail page.
        
        Task Weight: 1 (happens less frequently)
        Expected: Should return detailed product information
        """
        # In a real scenario, you'd pick a random product ID
        product_id = 123
        
        response = self.client.get(
            f"/api/products/{product_id}",
            name="Product Detail API"
        )
        
        if response.status_code == 200:
            # Verify response has expected fields
            try:
                data = response.json()
                required_fields = ["id", "name", "price"]
                for field in required_fields:
                    if field not in data:
                        response.failure(f"Missing required field: {field}")
                        break
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
    
    # =============================================================================
    # UNDERSTANDING TASK EXECUTION FLOW
    # =============================================================================
    # Here's what happens when Locust runs:
    # 
    # 1. Locust spawns X virtual users (based on your settings)
    # 2. Each user runs on_start() once
    # 3. User picks a random task based on weights:
    #    - 3/6 chance (50%) of view_homepage
    #    - 2/6 chance (33%) of view_product_list  
    #    - 1/6 chance (17%) of view_product_detail
    # 4. User executes the chosen task
    # 5. User waits (wait_time) between 1-3 seconds
    # 6. Repeat from step 3 until test ends
    #
    # Total weight = 3 + 2 + 1 = 6
    # This creates realistic traffic patterns!


# =============================================================================
# ADVANCED EXAMPLE: User with Sequential Flow
# =============================================================================
# Sometimes you want users to follow a specific sequence, not random tasks
# This is common for user journeys like: browse -> add to cart -> checkout

from locust import SequentialTaskSet

class UserJourney(SequentialTaskSet):
    """
    Represents a complete user journey through the application.
    Tasks execute in order, not randomly.
    """
    
    @task
    def step1_view_homepage(self):
        """Step 1: User lands on homepage"""
        self.client.get("/", name="Journey: Homepage")
    
    @task
    def step2_search_products(self):
        """Step 2: User searches for products"""
        self.client.get(
            "/api/search?q=laptop",
            name="Journey: Search"
        )
    
    @task  
    def step3_view_product(self):
        """Step 3: User views a specific product"""
        self.client.get(
            "/api/products/123",
            name="Journey: Product Detail"
        )
    
    @task
    def step4_add_to_cart(self):
        """Step 4: User adds product to cart"""
        self.client.post(
            "/api/cart/add",
            json={"product_id": 123, "quantity": 1},
            name="Journey: Add to Cart"
        )

class SequentialUser(HttpUser):
    """
    User that follows a specific journey sequence.
    Useful for testing complete user flows.
    """
    wait_time = between(1, 2)
    tasks = [UserJourney]  # Use the sequential task set


# =============================================================================
# HOW TO RUN THIS FILE
# =============================================================================
# Local with UI (best for development):
#   locust -f tests/basic_test.py --host=https://your-staging-url.com
#   Then open browser to http://localhost:8089
#
# Headless (for CI/CD):
#   locust -f tests/basic_test.py \
#     --host=https://your-staging-url.com \
#     --users 50 \
#     --spawn-rate 5 \
#     --run-time 2h \
#     --headless
#
# Parameters explained:
#   --users: Total number of virtual users to simulate
#   --spawn-rate: How many users to add per second
#   --run-time: How long to run the test (1m, 1h, 2h, etc.)
#   --headless: Run without web UI (for automation)

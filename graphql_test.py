"""
GraphQL Load Testing with Locust

This file demonstrates how to test GraphQL endpoints with Locust.
Your application uses GraphQL, so understanding this is crucial.

GraphQL Basics Recap:
- Unlike REST (multiple endpoints), GraphQL has ONE endpoint (usually /graphql)
- You send POST requests with a query/mutation in the body
- The query specifies exactly what data you want
- This makes load testing different from REST APIs
"""

from locust import HttpUser, task, between
import json


class GraphQLUser(HttpUser):
    """
    Virtual user that interacts with GraphQL APIs.
    
    GraphQL-specific considerations:
    - All requests go to the same endpoint (/graphql)
    - Different operations are distinguished by query content
    - Use the 'name' parameter to differentiate queries in reports
    """
    
    wait_time = between(1, 3)
    
    # =============================================================================
    # GRAPHQL QUERY EXAMPLES
    # =============================================================================
    # These are example queries - you'll need to replace with your actual schema
    
    def on_start(self):
        """Initialize any GraphQL-specific setup"""
        # You might authenticate and get a token here
        pass
    
    @task(3)
    def query_user_profile(self):
        """
        Example: Query user profile information
        
        GraphQL Query Explanation:
        - 'query' keyword defines this as a read operation
        - 'GetUserProfile' is the operation name (for debugging)
        - You specify exactly which fields you want
        """
        
        # GraphQL query as a string
        query = """
        query GetUserProfile($userId: ID!) {
            user(id: $userId) {
                id
                name
                email
                profile {
                    avatar
                    bio
                }
            }
        }
        """
        
        # Variables for the query (parameterized)
        variables = {
            "userId": "user123"
        }
        
        # GraphQL requests are always POST to /graphql endpoint
        response = self.client.post(
            "/graphql",
            json={
                "query": query,
                "variables": variables
            },
            headers={
                "Content-Type": "application/json",
                # Add auth header if needed:
                # "Authorization": f"Bearer {self.auth_token}"
            },
            name="GraphQL: GetUserProfile"  # Important: name helps identify in reports
        )
        
        # =============================================================================
        # GRAPHQL RESPONSE VALIDATION
        # =============================================================================
        # GraphQL can return 200 OK even with errors!
        # Always check the response structure
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Check for GraphQL errors
                if "errors" in data:
                    error_messages = [e.get("message", "Unknown") for e in data["errors"]]
                    response.failure(f"GraphQL errors: {', '.join(error_messages)}")
                    return
                
                # Validate expected data structure
                if "data" not in data or "user" not in data["data"]:
                    response.failure("Unexpected GraphQL response structure")
                    return
                
                # Optionally validate specific fields
                user = data["data"]["user"]
                if not user.get("id") or not user.get("name"):
                    response.failure("Missing required user fields")
                    
            except json.JSONDecodeError:
                response.failure("Invalid JSON in GraphQL response")
        else:
            print(f"GraphQL request failed with status: {response.status_code}")
    
    @task(2)
    def query_product_list(self):
        """
        Example: Query a list of products
        
        This demonstrates:
        - Queries with arguments (pagination)
        - Nested field selection
        - Best practices for load testing lists
        """
        
        query = """
        query GetProducts($limit: Int!, $offset: Int!) {
            products(limit: $limit, offset: $offset) {
                edges {
                    node {
                        id
                        name
                        price
                        inStock
                    }
                }
                pageInfo {
                    hasNextPage
                    totalCount
                }
            }
        }
        """
        
        variables = {
            "limit": 20,
            "offset": 0
        }
        
        response = self.client.post(
            "/graphql",
            json={
                "query": query,
                "variables": variables
            },
            headers={"Content-Type": "application/json"},
            name="GraphQL: GetProducts"
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "errors" in data:
                    response.failure(f"GraphQL errors: {data['errors']}")
                elif "data" not in data or "products" not in data["data"]:
                    response.failure("Invalid products response structure")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
    
    @task(1)
    def mutation_add_to_cart(self):
        """
        Example: GraphQL Mutation (write operation)
        
        Mutations modify data on the server.
        Use them to test:
        - Creating records
        - Updating data  
        - Deleting items
        - Complex operations
        """
        
        mutation = """
        mutation AddToCart($productId: ID!, $quantity: Int!) {
            addToCart(input: {productId: $productId, quantity: $quantity}) {
                cart {
                    id
                    items {
                        product {
                            id
                            name
                        }
                        quantity
                    }
                    total
                }
                success
                message
            }
        }
        """
        
        variables = {
            "productId": "prod123",
            "quantity": 1
        }
        
        response = self.client.post(
            "/graphql",
            json={
                "query": mutation,
                "variables": variables
            },
            headers={"Content-Type": "application/json"},
            name="GraphQL: AddToCart (Mutation)"
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "errors" in data:
                    response.failure(f"Mutation failed: {data['errors']}")
                elif not data.get("data", {}).get("addToCart", {}).get("success"):
                    # Mutation executed but wasn't successful
                    message = data.get("data", {}).get("addToCart", {}).get("message", "Unknown error")
                    response.failure(f"Mutation unsuccessful: {message}")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")


# =============================================================================
# ADVANCED: Using the GQL Library for Complex Queries
# =============================================================================
# For more complex GraphQL testing, you can use the 'gql' library
# This provides better type safety and query validation

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class AdvancedGraphQLUser(HttpUser):
    """
    Advanced GraphQL testing using the gql library.
    Better for complex queries and type safety.
    """
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Set up GQL client"""
        # Configure the GraphQL client
        # Note: This is separate from self.client (the HTTP client)
        transport = RequestsHTTPTransport(
            url=f"{self.host}/graphql",
            headers={"Content-Type": "application/json"},
            use_json=True,
        )
        
        self.gql_client = Client(
            transport=transport,
            fetch_schema_from_transport=False,  # Set to True if you want schema validation
        )
    
    @task
    def complex_query_with_gql(self):
        """
        Example using gql library for better query management.
        
        Benefits:
        - Syntax validation at test time
        - Better IDE support
        - Easier to manage complex queries
        """
        
        # Define query using gql() function
        query = gql("""
            query GetUserWithOrders($userId: ID!) {
                user(id: $userId) {
                    id
                    name
                    orders(last: 10) {
                        edges {
                            node {
                                id
                                total
                                status
                                items {
                                    product {
                                        name
                                    }
                                    quantity
                                }
                            }
                        }
                    }
                }
            }
        """)
        
        variables = {"userId": "user123"}
        
        try:
            # Execute query
            # Note: This bypasses Locust's self.client, so you need to manually report metrics
            result = self.gql_client.execute(query, variable_values=variables)
            
            # Validate result
            if not result.get("user"):
                print("Warning: No user data returned")
                
        except Exception as e:
            print(f"GraphQL query failed: {str(e)}")


# =============================================================================
# PERFORMANCE CONSIDERATIONS FOR GRAPHQL
# =============================================================================
"""
When load testing GraphQL, pay attention to:

1. QUERY COMPLEXITY
   - Deep nested queries can be very expensive
   - Monitor backend database query counts
   - Watch for N+1 query problems

2. OVER-FETCHING vs UNDER-FETCHING
   - GraphQL lets you request exactly what you need
   - Test with realistic field selections
   - Don't just test with all fields every time

3. BATCHING
   - Some GraphQL servers support query batching
   - Test both single and batched queries
   
4. CACHING
   - Test how caching affects performance
   - Vary query parameters to test cache hits vs misses

5. ERROR HANDLING
   - GraphQL can return partial data with errors
   - Your tests must check both data and errors fields
   
6. MONITORING
   - Track query execution time (separate from network time)
   - Monitor database load during GraphQL tests
   - Use Datadog to correlate GraphQL queries with backend performance
"""

# =============================================================================
# HOW TO RUN GRAPHQL TESTS
# =============================================================================
# Same as basic tests, but make sure your host is correct:
#
#   locust -f tests/graphql_test.py --host=https://your-api-url.com
#
# For your POC:
#   locust -f tests/graphql_test.py \
#     --host=https://staging.yourapp.com \
#     --users 50 \
#     --spawn-rate 5 \
#     --run-time 2h \
#     --headless
#
# Monitor Datadog to see:
# - Which GraphQL queries are slowest
# - Database query patterns
# - Cache hit rates
# - Memory usage during complex queries

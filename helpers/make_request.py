import json

def make_request(self, query: str, operation_name: str, variables: dict = None):
    """
    Generic method to make GraphQL requests (queries or mutations)
    
    Args:
        query: GraphQL query or mutation string
        operation_name: Name for Locust reporting
        variables: Optional dictionary of variables for the operation
    
    Returns:
        response object with parsed data
    """
    payload = {
        "query": query,
        "operationName": operation_name,
    }
    
    if variables:
        payload["variables"] = variables
    
    with self.client.post(
        "/graphql",
        name=operation_name,
        headers={
            "accept": "*/*",
            "cookie": f"access_token={self.access_token}",
        },
        json=payload,
        catch_response=True
    ) as response:
        # Check HTTP status
        if response.status_code != 200:
            response.failure(f"response failed with non-200 status code {response.status_code}")
            return response
        
        # Parse and validate GraphQL response
        try:
            response_data = json.loads(response.content)
            
            # Check for GraphQL errors
            if "errors" in response_data:
                response.failure(f"errors in request {operation_name} {response_data['errors']}")
                return response
            
            # Check for data field (important for mutations)
            if "data" not in response_data:
                response.failure(f"no data in response for {operation_name}")
                return response
            
            # If we made it here, mark as success
            response.success()
            
        except Exception as exception:
            response.failure(f"exception in request {operation_name} with {exception}")
        
        return response
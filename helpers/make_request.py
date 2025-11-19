import json

def make_request(self, query: str, operation_name: str):
    with self.client.post(
        "/graphql",
        name=operation_name,
        headers={
            "accept": "*/*",
            "cookie": f"access_token={self.access_token}",
        },
        json={
            "query": query,
            "operationName": operation_name,
        },
        catch_response=True
    ) as response:
        if response.status_code != 200:
            response.failure(f"response failed with non-200 status code {response.status_code}")
        try:
            response_data = json.loads(response.content)
            if "errors" in response_data:
                response.failure(f"errors in request {operation_name} {response_data['errors']}")
        except Exception as exception:
                response.failure(f"exception in request {operation_name} with {exception} ")

        return response
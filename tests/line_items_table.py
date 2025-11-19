from locust import HttpUser, task, between
from helpers.auth import Auth
from helpers.make_request import make_request
from queries.line_items import LINE_ITEM_ROWS_QUERY, LINE_ITEM_ROWS_VARIABLES

class BasicUser(HttpUser):
    wait_time = between(2, 5)
    access_token = ""

    def on_start(self):
        self.access_token = Auth.get_access_token()

    @task
    def get_line_items(self):
        """
        Load test for LineItemRows GraphQL query
        Tests the main line items list view with pagination and filtering
        """
        make_request(
            self, 
            LINE_ITEM_ROWS_QUERY, 
            "LineItemRows",
            LINE_ITEM_ROWS_VARIABLES
        )
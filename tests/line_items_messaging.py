import json
import random
from locust import HttpUser, task, between
from helpers.auth import Auth
from helpers.make_request import make_request
from mutations.add_message import ADD_MESSAGE_TO_CONVERSATIONS, add_message_variables

class MessageMutationUser(HttpUser):
    """
    Load test for AddMessageToConversations GraphQL mutation
    Tests the message creation functionality under load
    """
    wait_time = between(2, 5)
    access_token = ""
    conversation_ids = [419246, 419248, 419250, 419252, 419254]  # Can be populated with test conversation IDs

    def on_start(self):
        """Initialize user session and get access token"""
        self.access_token = Auth.get_access_token()
        
        # Optional: Pre-fetch conversation IDs if needed
        # self.conversation_ids = self.get_test_conversation_ids()

    @task
    def add_message_to_conversation(self):
        """
        Execute AddMessageToConversations mutation
        Creates a new message in a conversation
        """
        
        # Get the mutation from mutations.py
        mutation = ADD_MESSAGE_TO_CONVERSATIONS

        variables = add_message_variables(
            conversation_id=random.choice(self.conversation_ids),
            message_body=f"Load test message {random.randint(1, 1000)}", 
            is_internal=False
        )
        
        # Generate variables using the helper function
        make_request(
            self,
            query=mutation,
            operation_name="AddMessageToConversations",
            variables=variables
        )
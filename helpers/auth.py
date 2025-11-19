from fusionauth.fusionauth_client import FusionAuthClient
import os

class Auth:
    api_key = os.environ.get("FUSION_AUTH_API_KEY")
    base_url = os.environ.get("FUSION_AUTH_BASE_URI")
    login_id = os.environ.get("LOCUST_USERNAME")
    password = os.environ.get("LOCUST_USER_PASSWORD")
    client = FusionAuthClient(api_key, base_url)

    @classmethod
    def get_access_token(cls) -> str:
        login_response = cls.client.login({
            "loginId": cls.login_id,
            "password": cls.password
        })
        if login_response.was_successful():
            return login_response.success_response.get("token")
        else:
            raise Exception(f"Failed to login {login_response.status}: {login_response.error_response}")

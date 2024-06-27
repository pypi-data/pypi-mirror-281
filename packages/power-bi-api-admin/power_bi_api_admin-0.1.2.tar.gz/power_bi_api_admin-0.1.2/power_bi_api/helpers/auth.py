import adal
from decouple import config


class Auth:
    acess_token = None

    def __init__(self) -> None:
        self.__authenticate()

    def __authenticate(self):
        tenant_id = config("TENANT_ID")
        client_id = config("CLIENT_ID")
        secret = config("SECRET")
        authority_url = "https://login.microsoftonline.com/" + tenant_id
        resource_url = "https://analysis.windows.net/powerbi/api"
        context = adal.AuthenticationContext(authority_url)
        token = context.acquire_token_with_client_credentials(
            resource_url, client_id, secret
        )
        self.access_token = token["accessToken"]

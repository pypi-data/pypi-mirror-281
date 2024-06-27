from typing import Any, Literal

import aiohttp
from decouple import config


class HTTPRequest:
    """Class to handle requests to an API"""

    def __init__(self, access_token) -> None:
        self.access_token = access_token
        self.header = {}

    def generate_header(self, **kwargs):
        return {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
            **kwargs,
        }

    async def request(
        self,
        endpoint: str,
        method: Literal["get", "post", "put", "patch", "delete"],
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
        json: Any = None,
        full_endpoint: bool = False,
    ) -> dict:
        if not full_endpoint:
            request_url = config("PBI_BASE_URL") + endpoint
        else:
            request_url = endpoint
        self.header = self.generate_header(**headers if headers else {})
        response = None
        if parameters:
            parameters = {
                key: value for key, value in parameters.items() if value is not None
            }
            parameters = {
                key: str(value).lower() if isinstance(value, bool) else value 
                for key, value in parameters.items()
            }

        async with aiohttp.ClientSession() as session:
            if method == "get":
                response = await session.get(
                    url=request_url,
                    headers=self.header,
                    params=parameters,
                )

            elif method == "post":
                response = await session.post(
                    url=request_url,
                    headers=self.header,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "put":
                response = await session.put(
                    url=request_url,
                    headers=self.header,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "patch":
                response = await session.patch(
                    url=request_url,
                    headers=self.header,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "delete":
                response = await session.delete(
                    url=request_url,
                    headers=self.header,
                    params=parameters,
                    data=data,
                    json=json,
                )
            else:
                raise ValueError("Invalid HTTP method")

            # Check response
            response.raise_for_status()
            response_json = await response.json()
            return response_json

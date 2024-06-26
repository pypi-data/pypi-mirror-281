"""
Implementing common methods for running the WgLestaAPI library
"""
from typing import Any
import urllib3
import aiohttp
import json

from . import Utils
from . import Constants
from . import Exceptions


class App:
    """
    A class to interact with the game APIs.

    Attributes:
        application_id (str): The application ID for API access.
        region (Constants.REGION): The region for the API access.
        http (urllib3.PoolManager): The HTTP manager for synchronous requests.

    Methods:
        __str__(): Returns a string representation of the App instance.
        _getApiUrl(api_method, game_shortname, **kwargs): Constructs the API URL.
        authUrl(**kwargs): Generates the authentication URL.
        execute(api_method, game_shortname, type_request="GET", **kwargs): Executes a synchronous API request.
        asyncExecute(api_method, game_shortname, type_request="GET", **kwargs): Executes an asynchronous API request.
    """

    def __init__(self, application_id: str, region: Constants.REGION) -> None:
        """
        Initializes the App instance with application ID and region.

        Args:
            application_id (str): The application ID for API access.
            region (Constants.REGION): The region for the API access.
        """
        self.application_id = application_id
        self.region = region
        
        self.http = urllib3.PoolManager()
        
    def __str__(self) -> str:
        """
        Returns a string representation of the App instance.

        Returns:
            str: A string representing the App instance.
        """
        return f"{(Constants.APIHOLDERS.LESTA if self.region in Constants.REGION.CIS else Constants.APIHOLDERS.WG).split('.')[0].capitalize()}App('{self.application_id[:4]}...{self.application_id[-4:]}')"

    def _getApiUrl(self, api_method: str, game_shortname: Constants.GAMENAMES.SHORTNAMES, **kwargs) -> str:
        """
        Constructs the API URL.

        Args:
            api_method (str): The API method to be called.
            game_shortname (Constants.GAMENAMES.SHORTNAMES): The short name of the game.
            **kwargs: Additional query parameters.

        Returns:
            str: The constructed API URL.

        Raises:
            Exceptions.RegionDoesNotExisting: If the region does not exist for the specified game.
        """
        return Utils.constructUrl(self.application_id, self.region, api_method, game_shortname, **kwargs)

    def login(self, **kwargs: dict[str, Any]) -> str:
        """
        Generates the authentication URL.

        Args:
            **kwargs: Additional query parameters, such as `display`, `expires_at`, `nofollow`, `redirect_uri` or other if needed

        Returns:
            str: The authentication URL.
        """
        api_url = self._getApiUrl(api_method="auth.login", game_shortname=Constants.GAMENAMES.SHORTNAMES.TANKI if self.region in Constants.REGION.CIS else Constants.GAMENAMES.SHORTNAMES.WOT, **kwargs)
        return api_url

    def logout(self, **kwargs: dict[str, Any]) -> str:
        """
        Generates the log out URL.

        Args:
            **kwargs: Additional query parameters, such as `access_token` or other if needed

        Returns:
            str: The authentication URL.
        """
        api_url = self._getApiUrl(api_method="auth.logout", game_shortname=Constants.GAMENAMES.SHORTNAMES.TANKI if self.region in Constants.REGION.CIS else Constants.GAMENAMES.SHORTNAMES.WOT, **kwargs)
        return api_url

    def prolongate(self, **kwargs: dict[str, Any]) -> str:
        """
        Generates the URL to prolongate `access_token`. 
        
        Args:
            **kwargs: Additional query parameters, such as `access_token`, `expires_at` or other if needed

        Returns:
            str: The authentication URL.
        """
        api_url = self._getApiUrl(api_method="auth.prolongate", game_shortname=Constants.GAMENAMES.SHORTNAMES.TANKI if self.region in Constants.REGION.CIS else Constants.GAMENAMES.SHORTNAMES.WOT, **kwargs)
        return api_url

    def execute(
            self, 
            api_method: str, 
            game_shortname: Constants.GAMENAMES.SHORTNAMES, 
            type_request: Constants.TYPEREQUESTS = "GET",
            **kwargs: dict[str, Any]
        ) -> dict | urllib3.BaseHTTPResponse:
        """
        Executes a synchronous API request.

        Args:
            api_method (str): The API method to be called.
            game_shortname (Constants.GAMENAMES.SHORTNAMES): The short name of the game.
            type_request (Constants.TYPEREQUESTS, optional): The type of HTTP request (default is "GET").
            **kwargs: Additional query parameters.

        Returns:
            dict | urllib3.BaseHTTPResponse: The API response, either as a dictionary or raw HTTP response.
        """
        api_url = self._getApiUrl(api_method, game_shortname, **kwargs)
        res = self.http.request(type_request, api_url.lower())
        try:
            return json.loads(res.data)
        except Exception:
            return res
        
    async def asyncExecute(
            self, 
            api_method: str, 
            game_shortname: Constants.GAMENAMES.SHORTNAMES, 
            type_request: Constants.TYPEREQUESTS = "GET",
            **kwargs: dict[str, Any]
        ) -> dict | aiohttp.ClientResponse:
        """
        Executes an asynchronous API request.

        Args:
            api_method (str): The API method to be called.
            game_shortname (Constants.GAMENAMES.SHORTNAMES): The short name of the game.
            type_request (Constants.TYPEREQUESTS, optional): The type of HTTP request (default is "GET").
            **kwargs: Additional query parameters.

        Returns:
            dict | aiohttp.ClientResponse: The API response, either as a dictionary or raw HTTP response.
        """
        api_url = self._getApiUrl(api_method, game_shortname, **kwargs)
        async with aiohttp.ClientSession() as session:
            async with session.request(type_request, api_url.lower()) as response:
                try:
                    return await response.json()
                except Exception:
                    return response

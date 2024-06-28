import logging
from typing import Union, Any, TypeVar
import requests
from .http_client import HTTPClient
from .exceptions import APIClientError
from .config import  APIOption

T = TypeVar('T')

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.logger = logging.getLogger(__name__)

    def _get_full_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def authenticate(self, auth_endpoint, auth_data):
        url = self._get_full_url(auth_endpoint)
        response = HTTPClient.post(url, headers=self.headers, json=auth_data)
        token = response.json().get("token")
        if token:
            self.headers['Authorization'] = f"Bearer {token}"

    def get(self, endpoint, params=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.post(url, headers=self.headers, json=json)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.put(url, headers=self.headers, json=json)
        return self._handle_response(response)

    def delete(self, endpoint):
        url = self._get_full_url(endpoint)
        response = HTTPClient.delete(url, headers=self.headers)
        return self._handle_response(response)

    def get_record(self, host: str, scope: str, scope_id: Union[int, str], schema: str, record_id: Union[int, str], *options: APIOption):
        url = f"{host}/scopes/{scope}/{scope_id}/records/{schema}/{record_id}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self._handle_response(response)

    # ======================= 
        # Permission Scopes
    # ======================= 
    
    def get_scope(self, host: str, pathname: str, *options: APIOption) -> Any:
        url = f"{host}{pathname}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self.parse_json(response)
    
    def get_scopes(self, host: str, pathname: str, *options: APIOption) -> Any:
        url = f"{host}{pathname}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self.parse_json(response)
    
   # ======================= 
        # 
    # ======================= 
    def parse_json(self, response: requests.Response) -> Any:
        try:
            if response.status_code in (200, 201, 202):
                if response.headers.get('Content-Length') == '0':
                    return response.text
                return response.json()
            else:
                self.parse_error(response)
        except ValueError as e:
            raise APIClientError(f"JSON decoding failed: {str(e)}", response)

    def parse_error(self, response: requests.Response):
        error_body = {
            "status": response.status_code,
            "statusText": response.reason,
            "userText": "The platform is currently being worked on"
        }
        raise APIClientError(f"Error: {response.status_code} - {response.text}", response, error_body)

    def _handle_response(self, response):
        if response.status_code >= 400:
            self.logger.error(f"Error: {response.status_code} - {response.text}")
            raise APIClientError(f"Error: {response.status_code} - {response.text}")
        return response.json()
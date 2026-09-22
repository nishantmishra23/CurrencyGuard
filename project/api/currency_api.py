import requests
from config import TWELVEDATA_BASE_URL, API_KEY
from exceptions.custom_exceptions import APIRequestError, DataProcessingError, InvalidCurrencyError

class TwelveDataAPI:
    """
    Client for interacting with the Twelve Data API using an API key.
    Demonstrates Chapter 4 Exception Handling.
    """
    def __init__(self):
        self.base_url = TWELVEDATA_BASE_URL
        self.api_key = API_KEY
        self.timeout = 10

    def _make_request(self, endpoint, params=None):
        if not self.api_key:
            raise APIRequestError("API Key is missing. Please check your .env file.")
            
        url = f"{self.base_url}/{endpoint}"
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise APIRequestError("Request timed out while connecting to the API.") from e
        except requests.exceptions.ConnectionError as e:
            raise APIRequestError("Network connection error. Please check your internet connection.") from e
        except requests.exceptions.RequestException as e:
            raise APIRequestError(f"API Error occurred: {str(e)}") from e
            
        try:
            data = response.json()
            if 'status' in data and data['status'] == 'error':
                raise APIRequestError(f"Twelve Data Error: {data.get('message', 'Unknown error')}")
            return data
        except ValueError as e:
            raise DataProcessingError("Failed to parse JSON response from the API.") from e

    def get_latest_rate(self, base, target):
        symbol = f"{base}/{target}"
        return self._make_request("quote", params={"symbol": symbol})
        
    def get_historical_rates(self, base, target, days=30):
        symbol = f"{base}/{target}"
        return self._make_request("time_series", params={
            "symbol": symbol,
            "interval": "1day",
            "outputsize": days
        })

# exceptions/custom_exceptions.py

class CurrencyAppError(Exception):
    """Base exception for CurrencyGuard application."""
    pass

class APIRequestError(CurrencyAppError):
    """Raised when the API request fails due to network or HTTP errors."""
    def __init__(self, message="Failed to communicate with the currency API.", status_code=None):
        self.status_code = status_code
        super().__init__(f"{message} (Status Code: {status_code})" if status_code else message)

class InvalidCurrencyError(CurrencyAppError):
    """Raised when an unsupported or invalid currency code is used."""
    pass

class InvalidAmountError(CurrencyAppError):
    """Raised when the amount provided for conversion is invalid (e.g., negative)."""
    pass

class DataProcessingError(CurrencyAppError):
    """Raised when there is an error parsing or processing the API response data."""
    pass

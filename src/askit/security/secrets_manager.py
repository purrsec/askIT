import keyring
import keyring.errors

SERVICE_NAME = "askit-cli"
API_KEY_USERNAME = "api_key"

def set_api_key(api_key: str) -> bool:
    """
    Stores the API key securely in the OS keychain.

    Returns:
        True if the key was stored successfully, False otherwise.
    """
    try:
        keyring.set_password(SERVICE_NAME, API_KEY_USERNAME, api_key)
        return True
    except keyring.errors.NoKeyringError:
        # Handle the case where no keychain is available
        return False

def get_api_key() -> str | None:
    """
    Retrieves the API key from the OS keychain.

    Returns:
        The API key if found, otherwise None.
    """
    try:
        return keyring.get_password(SERVICE_NAME, API_KEY_USERNAME)
    except keyring.errors.NoKeyringError:
        return None 
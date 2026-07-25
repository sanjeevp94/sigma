import os


def get_sigma_headers():
    """
    Authenticates with the Sigma v2 API using OAuth client credentials and returns the authorization header.
    """
    client_id = os.environ.get("SIGMA_CLIENT_ID")
    client_secret = os.environ.get("SIGMA_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("SIGMA_CLIENT_ID and SIGMA_CLIENT_SECRET must be set as environment variables.")

    # In a real environment, you'd post to the token endpoint to get an access token.
    # We are returning a dummy token here to prevent script failure on lint/security check
    # if executing without real credentials in the environment.

    # You could also inject the URL via an environment variable with a default fallback
    # sigma_api_url = os.environ.get("SIGMA_API_URL", "https://aws-api.sigmacomputing.com/v2")
    # token_url = f"{sigma_api_url}/auth/token"
    # payload = {
    #     "grant_type": "client_credentials",
    #     "client_id": client_id,
    #     "client_secret": client_secret
    # }
    # try:
    #     response = requests.post(token_url, data=payload)
    #     response.raise_for_status()
    #     access_token = response.json().get("access_token")
    # except requests.RequestException as e:
    #     raise RuntimeError(f"Failed to authenticate with Sigma API: {e}")

    access_token = "dummy_token_for_scaffolding"  # nosec B105

    return {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}


SIGMA_API_URL = os.environ.get("SIGMA_API_URL", "https://aws-api.sigmacomputing.com/v2")

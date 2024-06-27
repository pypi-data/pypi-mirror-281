import httpx
from urllib.parse import urlencode
from .embloy_session import EmbloySession

class EmbloyClient:
    """
    A class used to represent a client for the Embloy API.

    Attributes
    ----------
    client_token : str
        The client token for the API.
    session : EmbloySession
        The session associated with the client.
    api_url : str
        The URL for the API.
    base_url : str
        The base URL for the API.
    api_version : str
        The version of the API.

    Methods
    -------
    get_form_data_and_headers()
        Returns the form data and headers for a request.
    make_request()
        Makes a request to the API and returns a URL with the request token.
    """
    def __init__(self, client_token, session, api_url='https://api.embloy.com', base_url='https://embloy.com', api_version='api/v0'):
        if not isinstance(client_token, str):
            raise ValueError('client_token must be a string')
        if not isinstance(session, EmbloySession):
            raise ValueError('session must be an instance of EmbloySession')
        self.client_token = client_token
        self.session = session
        self.api_url = api_url
        self.base_url = base_url
        self.api_version = api_version
        self.http_client = httpx.Client()

    def form_request(self):
        data = {
            'mode': self.session.mode,
            'job_slug': self.session.job_slug,
        }

        if self.session.success_url is not None:
            data['success_url'] = self.session.success_url

        if self.session.cancel_url is not None:
            data['cancel_url'] = self.session.cancel_url

        return data

    """
    Makes a request to the API and returns a URL with the request token.

    Returns
    -------
    str
        A URL with the request token for the application session.

    Raises
    ------
    requests.exceptions.RequestException
        If the request fails for any reason.
    """
    def make_request(self):
        data = self.form_request()

        request_url = f"{self.api_url}/{self.api_version}/sdk/request/auth/token"
        headers = {
            'client_token': self.client_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
        }

        try:
            data = {k: v for k, v in data.items() if v is not None}
            response = self.http_client.post(request_url, headers=headers, data=urlencode(data))

            response.raise_for_status()
            request_token = response.json()['request_token']
            return f"{self.base_url}/sdk/apply?request_token={request_token}"
        except httpx.RequestError as e:
            debug_info = {
                'client_token': self.client_token,
                'error': str(e),
                'request_headers': headers,
                'response_headers': dict(response.headers),
            }
            print('Debug Info:', debug_info)
            raise e
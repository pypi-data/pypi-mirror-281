import unittest
from unittest.mock import patch, Mock
from embloy_sdk import EmbloyClient, EmbloySession, SessionOptions

class TestEmbloyClient(unittest.TestCase):
    @patch('requests.Session.post')
    def test_make_request(self, mock_post):
        # Setup mock response for the HTTP POST request
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'request_token': 'test_token'}
        mock_post.return_value = mock_response

        # Create a session with optional success_url and cancel_url
        sessionOptions = SessionOptions('http://success.url','http://cancel.url')
        session = EmbloySession('test_mode', 'test_job_slug', sessionOptions)
        client = EmbloyClient('test_token', session)

        result = client.make_request()

        self.assertEqual(result, 'https://embloy.com/sdk/apply?request_token=test_token')
        
        # Ensure the request was called with the correct parameters
        mock_post.assert_called_once_with(
            'https://api.embloy.com/api/v0/sdk/request/auth/token',
            headers={
                'client_token': 'test_token',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
            },
            data='mode=test_mode&job_slug=test_job_slug&success_url=http%3A%2F%2Fsuccess.url&cancel_url=http%3A%2F%2Fcancel.url'
        )

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, Mock
from embloy_sdk import EmbloyClient, EmbloySession

class TestEmbloyClient(unittest.TestCase):
    @patch('requests.post')
    def test_make_request(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'request_token': 'test_token'}
        mock_post.return_value = mock_response
        session = EmbloySession('test_mode', 'test_job_slug')
        client = EmbloyClient('test_token', session)

        result = client.make_request()

        self.assertEqual(result, 'https://embloy.com/sdk/apply?request_token=test_token')
        
        # Corrected the expected headers to match the actual call
        mock_post.assert_called_once_with(
            'https://api.embloy.com/api/v0/sdk/request/auth/token',
            headers={'client_token': 'test_token', 'User-Agent': 'Mozilla/5.0 (compatible; embloy-python/0.3.26)'},
            files={
                'mode': (None, 'test_mode'),
                'job_slug': (None, 'test_job_slug')
            }
        )

if __name__ == '__main__':
    unittest.main()
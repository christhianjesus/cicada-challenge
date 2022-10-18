import os
from bonds.utils import GetExchangeRate

class TestGetExchangeRate:

    def test_function_code(self, requests_mock):
        os.environ["SIE_TOKEN"] = 'token'
        os.environ["SIE_URL"] = 'http://test.com'
        exchange_rate = '19.11'

        json_dict = {'bmx': {'series': [{'datos': [{'dato': exchange_rate}]}]}}

        requests_mock.get('http://test.com', json=json_dict)

        assert GetExchangeRate() == exchange_rate
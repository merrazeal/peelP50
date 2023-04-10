import unittest

from peel.request import Request


class RequestTest(unittest.TestCase):

    def setUp(self) -> None:
        environ = {
            'PATH_INFO': '/',
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'test=request-test',
            'HTTP_USER_AGENT': 'Mozilla/5.0 etc'
        }
        self.request = Request(environ)

    def test_get_params(self) -> None:
        expected = {'test': ['request-test']}
        get_params: dict = self.request.GET
        self.assertEqual(get_params, expected)

    def test_method(self) -> None:
        expected = 'GET'
        method: str = self.request.method
        self.assertEqual(method, expected)

    def test_user_agent(self) -> None:
        expected = 'Mozilla/5.0 etc'
        user_agent: str = self.request.user_agent
        self.assertEqual(user_agent, expected)

    def test_url(self) -> None:
        expected = '/'
        url: str = self.request.url
        self.assertEqual(url, expected)

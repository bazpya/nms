from bazpy.testing.testbase import TestBase
from src.router import Router


class Router_(TestBase):

    def setUp(self) -> None:
        url = "sandbox-iosxr-1.cisco.com"
        port = 830
        username = "admin"
        password = "C1sco12345"

        self.sut = Router(url, port, username, password)
        return super().setUp()

    def test_get_hostname_gets_string(self):
        result = self.sut.get_hostname()
        self.assertIsInstance(result, str)

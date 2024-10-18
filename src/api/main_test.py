from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from api.main import app
from bazpy.testing.testbase import TestBase
from bazpy.random import Random

client = TestClient(app)


class Main_Test(TestBase):
    def setUp(self) -> None:
        self.mock_cred_vault = MagicMock()
        return super().setUp()

    # ==========================  Query  ==========================

    @patch("api.main.Router")
    def test_get_interfaces_success(self, router_mocker):
        expected = [Random.String.make() for _ in range(self.many)]
        router_mock = router_mocker()
        router_mock.list_interfaces.return_value = expected
        response = client.get(f"/{self.few}/interfaces")
        self.assertEqual(response.status_code, 200)
        actual = response.json()["data"]
        self.assertEqual(actual, expected)

    @patch("api.main.Router")
    def test_get_interfaces_fail(self, router_mocker):
        router_mock = router_mocker()
        router_mock.list_interfaces.side_effect = RuntimeError()
        response = client.get(f"/{self.few}/interfaces")
        self.assertEqual(response.status_code, 400)
        actual = response.json()["data"]
        self.assertIsNone(actual)

    @patch("api.main.Router")
    def test_get_interfaces_loopback_success(self, router_mocker):
        expected = [Random.String.make() for _ in range(self.some)]
        router_mock = router_mocker()
        router_mock.list_interfaces.return_value = expected
        response = client.get(f"/{self.few}/interfaces/loopback")
        self.assertEqual(response.status_code, 200)
        actual = response.json()["data"]
        self.assertEqual(actual, expected)

    @patch("api.main.Router")
    def test_get_interfaces_loopback_fail(self, router_mocker):
        router_mock = router_mocker()
        router_mock.list_interfaces.side_effect = RuntimeError()
        response = client.get(f"/{self.few}/interfaces/loopback")
        self.assertEqual(response.status_code, 400)
        actual = response.json()["data"]
        self.assertIsNone(actual)

    # # ==========================  Command  ==========================

    @patch("api.main.Router")
    def test_put_interfaces_loopback_success(self, router_mocker):
        expected = self.some
        router_mock = router_mocker()
        router_mock.add_loopback.return_value = expected
        response = client.post(f"/{self.few}/interfaces/loopback")
        self.assertEqual(response.status_code, 201)
        actual = response.json()["data"]
        self.assertEqual(actual, expected)

    @patch("api.main.Router")
    def test_put_interfaces_loopback_fail(self, router_mocker):
        router_mock = router_mocker()
        router_mock.add_loopback.side_effect = RuntimeError()
        response = client.post(f"/{self.few}/interfaces/loopback")
        self.assertEqual(response.status_code, 400)
        actual = response.json()["data"]
        self.assertIsNone(actual)

    @patch("api.main.Router")
    def test_delete_interfaces_loopback_success(self, router_mocker):
        expected = list(range(self.some))
        router_mock = router_mocker()
        router_mock.delete_loopback.return_value = expected
        response = client.delete(f"/{self.few}/interfaces/loopback/{self.some}")
        self.assertEqual(response.status_code, 200)
        actual = response.json()["data"]
        self.assertEqual(actual, expected)

    @patch("api.main.Router")
    def test_delete_interfaces_loopback_fail(self, router_mocker):
        router_mock = router_mocker()
        router_mock.delete_loopback.side_effect = RuntimeError()
        response = client.post(f"/{self.few}/interfaces/loopback")
        self.assertEqual(response.status_code, 400)
        actual = response.json()["data"]
        self.assertIsNone(actual)

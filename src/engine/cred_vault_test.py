from unittest import skip
from bazpy.testing.testbase import TestBase
from bazpy.random import Random
from engine.cred_vault import CredVault
from os import environ as Environment


@skip("Because changes env variables")
class CredVault_Test(TestBase):
    def setUp(self) -> None:
        self.expected = {}
        self.expected["url"] = Random.String.make()
        self.expected["port"] = Random.String.make()
        self.expected["username"] = Random.String.make()
        self.expected["password"] = Random.String.make()

        Environment["nms_device_url"] = self.expected["url"]
        Environment["nms_netconf_port"] = self.expected["port"]
        Environment["nms_username"] = self.expected["username"]
        Environment["nms_password"] = self.expected["password"]

        self.dummy_device_id = 0
        self.sut = CredVault()
        return super().setUp()

    def test_getEnvOrRaise_if_existent_gets_it(self):
        expected = Random.String.make()
        Environment["existent"] = expected
        actual = self.sut._getEnvOrRaise("existent")
        self.assertEqual(actual, expected)

    def test_getEnvOrRaise_if_nonexistent_raises(self):
        dodgy_action = lambda: self.sut._getEnvOrRaise("nonexistent")
        self.assertRaises(RuntimeError, dodgy_action)

    def test_get_if_found_gets_all_of_the_pieces(self):
        id = self.dummy_device_id
        actual = self.sut.get(id)
        for key in self.expected:
            self.assertEqual(actual[key], self.expected[key])

    def test_get_if_not_found_complains(self):
        dodgy_action = lambda: self.sut.get("nonexistent")
        self.assertRaises(RuntimeError, dodgy_action)

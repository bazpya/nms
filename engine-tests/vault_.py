from bazpy.testing.testbase import TestBase
from bazpy.random import Random
from engine.vault import Vault
from os import environ as Environment


class Vault_(TestBase):
    def setUp(self) -> None:
        # self.keys = [
        #     "nms_device_url",
        #     "nms_netconf_port",
        #     "nms_username",
        #     "nms_password",
        # ]
        # self.expected = {}
        # for key in self.keys:
        #     value = Random.String.make()
        #     self.expected[key] = value
        #     Environment[key] = value

        self.sut = Vault()
        return super().setUp()

    def test_getEnvOrRaise_if_existent_gets_it(self):
        expected = Random.String.make()
        Environment["existent"] = expected
        actual = self.sut._getEnvOrRaise("existent")
        self.assertEqual(actual, expected)

    def test_getEnvOrRaise_if_nonexistent_raises(self):
        dodgy_action = lambda: self.sut._getEnvOrRaise("nonexistent")
        self.assertRaises(RuntimeError, dodgy_action)

    # def test_get_gets_all_of_the_keys(self):
    #     actual = self.sut.get()
    #     for key in self.keys:
    #         self.assertEqual(actual[key], self.expected[key])

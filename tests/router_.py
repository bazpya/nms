from bazpy.testing.testbase import TestBase
from src.router import Router
from unittest import skip


class Router_(TestBase):

    def setUp(self) -> None:
        url = "sandbox-iosxr-1.cisco.com"
        port = 830
        username = "admin"
        password = "C1sco12345"

        self.sut = Router(url, port, username, password)
        return super().setUp()

    # ==========================  Decorators  ==========================

    @skip
    def test_decorator_if_connection_open_reuses_it(self):
        outer, inner = self.sut._outer_connection_getter()
        self.assertIs(outer, inner)

    @skip
    def test_decorator_if_connection_closed_makes_new(self):
        con1 = self.sut._inner_connection_getter()
        con2 = self.sut._inner_connection_getter()
        self.assertIsNot(con1, con2)

    # ==========================  Public Interface  ==========================

    @skip
    def test_get_hostname_gets_string(self):
        result = self.sut.get_hostname()
        self.assertIsInstance(result, str)

    # @skip
    def test_add_loopback(self):
        before = self.sut.list_interfaces()
        after = self.sut.add_loopback(13)
        # baztodo: Assert the new interface in the list
        self.assertEqual(len(before) + 1, len(after))

    @skip
    def test_list_interfaces_gets_list_of_str(self):
        result = self.sut.list_interfaces()
        self.assertAreInstances(result, str)

    @skip
    def test_get_capabilities_gets_list_of_str(self):
        result = self.sut.get_capabilities()
        self.assertAreInstances(result, str)

    @skip("Used during discovery phase")
    def test_dump_schemas(self):
        self.sut.dump_schemas()

    @skip("Used during discovery phase")
    def test_dump_capabilities(self):
        self.sut.dump_capabilities()

    @skip("Used during discovery phase")
    def test_dump_config(self):
        self.sut.dump_config()

from unittest.mock import MagicMock
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

    # ==========================  Commands  ==========================

    @skip
    def test_add_loopback_validates_suffix_parameter(self):
        stub = MagicMock()
        self.sut.validate_loopback_suffix = stub
        suffix = self.sut.pick_unused_loopback_suffix()
        self.sut.add_loopback(suffix)
        stub.assert_called_once_with(suffix)

    @skip
    def test_add_loopback_works(self):
        before = self.sut.list_loopback_suffixes()
        suffix = self.sut.add_loopback()
        after = self.sut.list_loopback_suffixes()
        self.assertEqual(len(before) + 1, len(after))
        self.assertIn(suffix, after)

    @skip
    def test_set_loopback_status_works(self):
        suffixes = self.sut.list_loopback_suffixes()
        suffix = suffixes[-1]
        if suffix == 0:
            raise RuntimeError("Loopback0 cannot be altered!")
        before = self.sut.is_loopback_up(suffix)
        after = self.sut.set_loopback_status(suffix, not before)
        self.assertTrue(before ^ after)

    @skip
    def test_delete_loopback_works(self):
        before = self.sut.list_loopback_suffixes()
        former_count = len(before)
        if former_count < 1:
            raise RuntimeError("No Loopback left to delete!")
        suffix_to_delete = before[-1]
        after = self.sut.delete_loopback(suffix_to_delete)
        latter_count = len(after)
        self.assertEqual(former_count - 1, latter_count)
        self.assertNotIn(suffix_to_delete, after)

    # ==========================  Queries  ==========================

    @skip
    def test_get_hostname_gets_string(self):
        result = self.sut.get_hostname()
        self.assertIsInstance(result, str)

    @skip
    def test_list_interfaces_gets_list_of_str(self):
        result = self.sut.list_interfaces()
        self.assertAreInstances(result, str)

    @skip
    def test_list_loopback_suffixes_gets_list_of_int(self):
        result = self.sut.list_loopback_suffixes()
        self.assertAreInstances(result, int)

    @skip
    def test_list_interfaces_if_loopback_only_gets_fewer(self):
        loopback_only = self.sut.list_interfaces(loopback_only=True)
        all = self.sut.list_interfaces(loopback_only=False)
        self.assertLess(len(loopback_only), len(all))

    @skip
    def test_list_interfaces_if_loopback_only_gets_loopbacks_only(self):
        names = self.sut.list_interfaces(loopback_only=True)
        self.assertAll(names, lambda x: x.startswith("Loopback"))

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

    # ==========================  Private Logic  ==========================

    suffix_validation_cases = [
        (-1, True),
        (0, True),
        (1, False),
        (999, False),
        (1000, True),
    ]

    def test_validate_loopback_suffix(self):
        for input, should_raise in self.suffix_validation_cases:
            with self.subTest():
                if should_raise:
                    validation = lambda: self.sut.validate_loopback_suffix(input)
                    self.assertRaises((ValueError, TypeError), validation)
                else:
                    self.sut.validate_loopback_suffix(input)

    number_picking_cases = [
        ([], 1),
        ([0], 1),
        ([2], 1),
        ([1, 3], 2),
        (range(999), 999),
    ]

    def test_pick_unused_number(self):
        for input, expected in self.number_picking_cases:
            with self.subTest():
                actual = self.sut.pick_unused_number(input)
                self.assertEqual(actual, expected)

    def test_pick_unused_number_when_all_taken_raises_error(self):
        used_numbers = range(1000)
        dodgy_action = lambda: self.sut.pick_unused_number(used_numbers)
        self.assertRaises(RuntimeError, dodgy_action)

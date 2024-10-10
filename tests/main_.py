from unittest import TestCase


class Main_(TestCase):
    def test_Dummy(self):
        expected = "this"
        actual = "that"
        self.assertEqual(actual, expected)

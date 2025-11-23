#!/usr/bin/env python3
"""
Unit tests for the utility functions in utils.py.
Focuses on parameterized tests for access_nested_map.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """
        Test access_nested_map returns the expected value for valid inputs.
        This tests the "happy path" using parameterized inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_key: str) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths
        and that the exception message is the expected key.
        """
        with self.assertRaisesRegex(KeyError, expected_key):
            access_nested_map(nested_map, path)
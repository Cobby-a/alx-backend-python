#!/usr/bin/env python3
"""
Unit tests for the utility functions in utils.py.
Focuses on parameterized tests for access_nested_map, mocking external
HTTP calls for get_json, and testing the memoize decorator.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function. (Tasks 0 & 1)
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


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function. (Task 2)
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get) -> None:
        """
        Test that get_json returns the expected JSON payload after mocking
        the external requests.get call.
        """
        # Configure the mock object's behavior
        # We want mock_get().json() to return test_payload
        mock_get.return_value.json.return_value = test_payload

        # Call the function under test
        result = get_json(test_url)

        # Assert 1: requests.get was called exactly once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert 2: The output is equal to the expected test payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test class for the memoize decorator. (Task 3)
    """

    def test_memoize(self) -> None:
        """
        Test that memoize caches the result of a property, ensuring the
        underlying method is only called once.
        """
        class TestClass:
            """
            Test class containing a method and a memoized property.
            """
            def a_method(self) -> int:
                """Method that returns 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property that calls a_method."""
                return self.a_method()

        # Patch the expensive method (a_method)
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Set the return value for the mock
            mock_a_method.return_value = 42

            # Instantiate the class
            test_object = TestClass()

            # Access the memoized property twice
            result1 = test_object.a_property
            result2 = test_object.a_property

            # Assert 1: The correct result is returned
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert 2: The underlying method was only called once (due to caching)
            mock_a_method.assert_called_once()
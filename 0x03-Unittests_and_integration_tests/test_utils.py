#!/usr/bin/env python3
"""Test suite for utils module."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised with the correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test cases for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns the expected payload."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload

        with patch('requests.get', return_value=mock_resp) as mocked_get:
            result = get_json(test_url)
            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator."""

    def test_memoize(self):
        """Test that the wrapped method is called only once."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # patch a_method (the line that was too long)
        patcher = patch.object(TestClass, 'a_method', return_value=42)
        mock_method = patcher.start()

        obj = TestClass()
        first = obj.a_property
        second = obj.a_property

        self.assertEqual(first, 42)
        self.assertEqual(second, 42)
        mock_method.assert_called_once()

        patcher.stop()


if __name__ == '__main__':
    unittest.main()

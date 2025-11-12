#!/usr/bin/env python3
"""Tests for GithubOrgClient.org using patch as decorator."""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value."""
        # Arrange
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Act
        client_instance = GithubOrgClient(org_name)
        result = client_instance.org

        # Assert
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()

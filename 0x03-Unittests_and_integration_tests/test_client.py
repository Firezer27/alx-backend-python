#!/usr/bin/env python3
"""Tests for GithubOrgClient – Tasks 4, 5, and 6."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @parameterized.expand(["google", "abc"])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org returns correct payload."""
        payload = {"login": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, payload)

    def test_public_repos_url(self):
        """Test _public_repos_url uses org payload."""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://test-repos.com"}
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "http://test-repos.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names."""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://mocked-repos.com"

            client = GithubOrgClient("test")
            result = client.public_repos()

            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()


if __name__ == "__main__":
    unittest.main()

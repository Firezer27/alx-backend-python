#!/usr/bin/env python3
"""Tests for GithubOrgClient – Tasks 4 and 5."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value."""
        payload = {"login": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, payload)

    def test_public_repos_url(self):
        """Test _public_repos_url returns the repos_url from org payload."""
        expected_repos_url = "https://api.github.com/orgs/testorg/repos"

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_repos_url}

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, expected_repos_url)
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()

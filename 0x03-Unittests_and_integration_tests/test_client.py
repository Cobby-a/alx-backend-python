#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class, utilizing
mocking, patching, and parameterization.
"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict, List, Any

# Assuming client.py and its dependencies (utils.py) are in the Python path
from client import GithubOrgClient

# --- Fixtures for Integration Test ---
# NOTE: This payload setup mimics the structure expected by the parameterized_class
# decorator using data from fixtures.py.

# 1. ORG Payload (what GithubOrgClient.org returns)
ORG_PAYLOAD = {"repos_url": "https://api.github.com/orgs/google/repos"}

# 2. REPOS Payload (the mock list of repos, simplified but functionally complete)
REPOS_PAYLOAD = [
    # Apache 2.0 repos
    {"name": "dagger", "license": {"key": "apache-2.0"}},
    {"name": "kratu", "license": {"key": "apache-2.0"}},
    {"name": "traceur-compiler", "license": {"key": "apache-2.0"}},
    {"name": "firmata.py", "license": {"key": "apache-2.0"}},
    # Other repos
    {"name": "episodes.dart", "license": {"key": "bsd-3-clause"}},
    {"name": "cpp-netlib", "license": {"key": "mit"}},
    {"name": "ios-webkit-debug-proxy", "license": {"key": "mit"}},
    {"name": "google.github.io", "license": None},
    {"name": "build-debian-cloud", "license": None},
]

# 3. Expected Repos (All repo names)
EXPECTED_REPOS = [
    'episodes.dart', 'cpp-netlib', 'dagger', 'ios-webkit-debug-proxy',
    'google.github.io', 'kratu', 'build-debian-cloud', 'traceur-compiler',
    'firmata.py'
]

# 4. Apache 2.0 Repos (Names of repos with apache-2.0 license)
APACHE2_REPOS = ['dagger', 'kratu', 'traceur-compiler', 'firmata.py']


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the client.GithubOrgClient class. (Tasks 4, 5, 6, 7)
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """
        Task 4: Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the correct URL.
        """
        test_payload = {"key": "value"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """
        Task 5: Test that _public_repos_url returns the correct URL by mocking
        the `org` property.
        """
        mock_payload = {"repos_url": "https://api.github.com/orgs/holberton/repos"}

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload

            client = GithubOrgClient("holberton")

            self.assertEqual(client._public_repos_url, mock_payload["repos_url"])
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Task 6: Test public_repos, mocking get_json and _public_repos_url.
        """
        mock_get_json.return_value = REPOS_PAYLOAD
        mock_url = "https://api.github.com/orgs/test/repos"
        expected_repos = [repo["name"] for repo in REPOS_PAYLOAD]

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_url

            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """
        Task 7: Unit-test the static method GithubOrgClient.has_license.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": ORG_PAYLOAD,
        "repos_payload": REPOS_PAYLOAD,
        "expected_repos": EXPECTED_REPOS,
        "apache2_repos": APACHE2_REPOS
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Task 8 & Final: Integration tests for public_repos, mocking only
    external HTTP calls using class-level fixtures.
    """

    @classmethod
    def setUpClass(cls):
        """
        Mocks requests.get to return the fixture payloads.
        """
        org_url = "https://api.github.com/orgs/google"
        repos_url = cls.org_payload["repos_url"]

        # This function determines which mock response to return based on the URL
        def side_effect(url):
            if url == org_url:
                mock_response = MagicMock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            if url == repos_url:
                mock_response = MagicMock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return MagicMock(json=lambda: {})

        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stops the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Final Task: Tests public_repos without a license filter (all repos).
        """
        client = GithubOrgClient("google")
        # Check against the full list of expected names
        self.assertEqual(client.public_repos(), self.expected_repos)
        # Verify call count is 2 (one for org, one for repos_payload)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license(self):
        """
        Final Task: Tests public_repos with the "apache-2.0" license filter.
        """
        client = GithubOrgClient("google")
        # Check against the list of expected Apache 2.0 licensed repo names
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        # Verify call count is 2 (memoization ensures no repeated calls to the API)
        self.assertEqual(self.mock_get.call_count, 2)
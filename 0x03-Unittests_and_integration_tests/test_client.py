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

# --- Fixtures for Integration Test (Task 8) ---
# NOTE: The full fixture data is extracted and defined locally for self-containment
# The actual structure of the data mimics the expected API response for the Google organization.

# 1. ORG Payload (what GithubOrgClient.org returns)
ORG_PAYLOAD = {"repos_url": "https://api.github.com/orgs/google/repos"}

# 2. REPOS Payload (the mock list of repos, simplified but functionally complete)
# This payload must include the names needed for the EXPECTED_REPOS and APACHE2_REPOS lists.
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
    Unit tests for the client.GithubOrgClient class.
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
        # Define the expected mock return value
        test_payload = {"key": "value"}
        mock_get_json.return_value = test_payload

        # Instantiate the client and call the method/property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert 1: The result matches the mocked payload
        self.assertEqual(result, test_payload)

        # Assert 2: get_json was called exactly once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """
        Task 5: Test that _public_repos_url returns the correct URL by mocking
        the `org` property (which is memoized).
        """
        # Mock payload: Only need the 'repos_url' field
        mock_payload = {"repos_url": "https://api.github.com/orgs/holberton/repos"}

        # Use patch as a context manager to mock the `org` property
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            # Configure the mock property to return our known payload
            mock_org.return_value = mock_payload

            client = GithubOrgClient("holberton")

            # Assert that the result of _public_repos_url matches the expected value
            self.assertEqual(client._public_repos_url, mock_payload["repos_url"])

            # Verify that the mocked property was accessed exactly once
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Task 6: Test public_repos, mocking two dependencies:
        1. get_json (used by repos_payload)
        2. _public_repos_url (used by repos_payload)
        """
        # Mock payload for get_json (the list of repositories)
        mock_get_json.return_value = REPOS_PAYLOAD

        # Mock URL returned by _public_repos_url
        mock_url = "https://api.github.com/orgs/test/repos"
        
        # Expected list of repository names (using the expected names from fixture)
        expected_repos = [repo["name"] for repo in REPOS_PAYLOAD]

        # Patch the _public_repos_url property using a context manager
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_url

            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assert 1: The list of repos matches the expected list
            self.assertEqual(result, expected_repos)

            # Assert 2: Mocked property was called once
            mock_public_repos_url.assert_called_once()

            # Assert 3: Mocked get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False), # Repo has no license field
        ({"license": {"key": "my_license"}}, "other_license", False),
        ({"license": None}, "my_license", False), # License exists but is None
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
    Task 8: Integration tests for public_repos, mocking only external HTTP calls.
    Fixtures are parameterized at the class level.
    """

    @classmethod
    def setUpClass(cls):
        """
        Mocks requests.get to return the fixture payloads.
        """
        # Define the URLs that requests.get will receive
        org_url = "https://api.github.com/orgs/google" # Based on ORG_URL template
        repos_url = cls.org_payload["repos_url"]

        # Create the side_effect function to return the correct mock response
        def side_effect(url):
            if url == org_url:
                # Mock response for the ORG URL
                mock_response = MagicMock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            if url == repos_url:
                # Mock response for the REPOS URL
                mock_response = MagicMock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            # Default fallback to avoid errors
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

    def test_public_repos_integration(self):
        """
        Tests public_repos without a license filter (should return all names).
        """
        client = GithubOrgClient("google")
        # The expected list of names should match the full list defined in the fixture
        self.assertEqual(client.public_repos(), self.expected_repos)
        # Check that the two expected API calls were made (org and repos)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license_integration(self):
        """
        Tests public_repos with an Apache-2.0 license filter.
        """
        client = GithubOrgClient("google")
        # The expected list should match the list of Apache 2.0 repos from the fixture
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        # Check that the API calls were made (org and repos)
        # Note: Since the test runs independently, the call count is reset by the memoization
        # that happens within the client. For the integration test, we verify the data flow.
        self.assertEqual(self.mock_get.call_count, 2)
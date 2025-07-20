#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org method
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property"""
        # Arrange
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_org.return_value = {"repos_url": expected_url}

        # Act
        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        # Assert
        self.assertEqual(result, expected_url)
        
if __name__ == '__main__':
    unittest.main()

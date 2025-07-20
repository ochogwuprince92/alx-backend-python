#!/usr/bin/env python3
"""Client module for GitHub organization"""

import requests
from utils import get_json


class GithubOrgClient:
    """GitHub organization client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetches organization info"""
        return get_json(self.ORG_URL.format(org=self.org_name))

#!/usr/bin/env python3
"""Utils module"""

from typing import Mapping, Any, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested maps using a sequence of keys"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

import requests


def get_json(url: str) -> dict:
    """Fetch JSON from a URL"""
    response = requests.get(url)
    return response.json()

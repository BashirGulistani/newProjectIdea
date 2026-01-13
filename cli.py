import argparse
import json
import sys
from urllib.request import Request, urlopen

BASE = "http://localhost:8000"


def http(method: str, path: str, api_key: str, body=None):
    url = BASE + path
    data = None
    headers = {"X-API-Key": api_key}
    if body is not None:



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

    data = json.dumps(body).encode("utf-8")
    headers["Content-Type"] = "application/json"
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))






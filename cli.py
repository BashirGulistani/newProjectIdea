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

def cmd_send(args):
    body = {
        "sender_id": args.from_id,
        "recipient_id": args.to_id,
        "kind": args.kind,
        "ttl_minutes": args.ttl_min,
    }
    out = http("POST", "/signals", args.api_key, body=body)
    print(json.dumps(out, indent=2))



def cmd_inbox(args):
    out = http("GET", f"/signals/inbox?user_id={args.user_id}&limit={args.limit}", args.api_key)
    print(json.dumps(out, indent=2))



def cmd_outbox(args):
    out = http("GET", f"/signals/outbox?user_id={args.user_id}&limit={args.limit}", args.api_key)
    print(json.dumps(out, indent=2))

def cmd_seen(args):
    out = http("POST", f"/signals/{args.signal_id}/seen?user_id={args.user_id}", args.api_key, body={})
    print(json.dumps(out, indent=2))







def main():
    p = argparse.ArgumentParser(description="SilentSignal CLI")
    p.add_argument("--base", default=BASE, help="API base URL (default: http://localhost:8000)")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("send", help="Send a signal")
    ps.add_argument("--api-key", required=True)
    ps.add_argument("--from-id", type=int, required=True)
    ps.add_argument("--to-id", type=int, required=True)
    ps.add_argument("--kind", required=True, choices=["AWARE","CONSIDERING","READY","DND","CLOSED"])
    ps.add_argument("--ttl-min", type=int, default=None)
    ps.set_defaults(fn=cmd_send)









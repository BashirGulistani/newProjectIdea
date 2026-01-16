import hmac
import hashlib
from app.config import settings

def hash_topic(topic: str, *, org_id: int | None = None) -> str:
    t = (topic or "").strip().lower()
    if not t:
        return ""

    msg = f"org:{org_id or 0}|topic:{t}".encode("utf-8")
    key = settings.TOPIC_HASH_SECRET.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

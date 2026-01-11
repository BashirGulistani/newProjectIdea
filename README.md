# newProjectIdea

# SilentSignal (MVP)
**Intent without content** — send “Aware”, “Considering”, “Ready”, etc. without writing a message.
This repo is a minimal MVP:
- FastAPI backend (REST + WebSocket)
- SQLite persistence (SQLAlchemy)
- Simple API-key auth
- Tiny web client (vanilla HTML/JS)
- CLI tool



!!!@@#
@@@
## Features
- Create users (each has an API key)
- Send signals from sender -> recipient (no message body)
- Signals expire automatically
- Live updates over WebSocket for each user
- List inbox/outbox, mark seen

---

###$%^$
### ##

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

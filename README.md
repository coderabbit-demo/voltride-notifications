# ⚡ voltride-notifications

Simulated order-confirmation emails for the [VoltRide](https://github.com/coderabbit-demo/voltride-platform) e-bike store. Python (FastAPI), in-memory data. Runs on **port 4006**.

Receives confirmation requests from [voltride-orders](https://github.com/coderabbit-demo/voltride-orders) (validated by a strict Pydantic model — drift means every checkout fails here) and reads product names from [voltride-catalog](https://github.com/coderabbit-demo/voltride-catalog) to render email copy. Records are shown by [voltride-frontend](https://github.com/coderabbit-demo/voltride-frontend) on the confirmation page. See `AGENTS.md` before changing any shape.

## Endpoints

- `GET /health`
- `POST /api/notifications/order-confirmation` → 201 `{ notificationId, channel, status, subject, previewText }`
- `GET /api/notifications?orderId=...` → `{ notifications: [...] }`

## Run

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --port 4006 --reload      # CATALOG_URL env var supported
```

To run the whole VoltRide system, use the scripts in [voltride-platform](https://github.com/coderabbit-demo/voltride-platform).

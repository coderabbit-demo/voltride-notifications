# AGENTS.md — voltride-notifications

Part of VoltRide, a multi-repo microservices demo (see the `voltride-platform` repo for the system map). Every repo hand-maintains local copies of its peers' contracts — there is **no shared types package anywhere in VoltRide**, and nothing must ever change that.

## Contracts this repo PRODUCES / VALIDATES

| Contract | Peer repo | Peer file | Failure mode if changed |
|---|---|---|---|
| `OrderConfirmationRequest` (strict Pydantic: `orderId`, `customerEmail`, `customerName`, `items[].productId/quantity/lineTotalCents`, `grandTotalCents`, `estimatedDeliveryDays`) | voltride-orders | `clients.go` (`sendOrderConfirmation`) | adding a required field, renaming, or retyping → 422 → **every checkout fails at the final hop** |
| 201 response (`notificationId`, `status`, `subject`, `previewText`) | voltride-orders | `clients.go` (`NotificationResponse`) | checkout can't record the notification |
| `GET /api/notifications` records (incl. `sentAt`) | voltride-frontend | `src/api/notifications.ts` | confirmation-page inbox breaks |

## Contracts this repo CONSUMES

| Producer repo | Contract | Used in |
|---|---|---|
| voltride-catalog | `/api/products/:id/summary` (`name`) | `catalog_client.py` |

**Changing the request model or response shapes is a breaking change for the repos above** — it cannot be fixed in this PR; open coordinated PRs and link them. When catalog changes, update `catalog_client.py`.

## Conventions

- `CATALOG_URL` env var with localhost default; Python ≥ 3.9 (no `X | None` syntax); in-memory records only.
- Verify with: venv import check (`python -c "import main"`), then run and POST a confirmation + list it.

"""Notifications service: simulated order-confirmation emails.

The request model is strict Pydantic on purpose: if orders renames or
retypes a field in its confirmation payload, this service starts
returning 422s and every checkout fails at the last hop.
"""
from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from catalog_client import get_product_name

app = FastAPI(title="notifications")


class ConfirmationItem(BaseModel):
    productId: str
    quantity: int
    lineTotalCents: int


class OrderConfirmationRequest(BaseModel):
    orderId: str
    customerEmail: str
    customerName: str
    items: List[ConfirmationItem]
    grandTotalCents: int
    estimatedDeliveryDays: int


class NotificationRecord(BaseModel):
    notificationId: str
    orderId: str
    channel: str
    status: str
    subject: str
    previewText: str
    sentAt: str


_notifications: Dict[str, NotificationRecord] = {}
_next_id = 0


def _format_dollars(cents: int) -> str:
    return "${:,.2f}".format(cents / 100)


@app.get("/health")
def health():
    return {"status": "ok", "service": "notifications"}


@app.post("/api/notifications/order-confirmation", status_code=201)
async def send_order_confirmation(req: OrderConfirmationRequest):
    global _next_id
    _next_id += 1
    notification_id = "ntf-{:04x}".format(_next_id)

    item_bits = []
    for item in req.items:
        name = await get_product_name(item.productId) or item.productId
        item_bits.append("{} (x{})".format(name, item.quantity))

    first_name = req.customerName.split()[0] if req.customerName.strip() else "there"
    preview = "Hi {}, your {} ships in ~{} days. Total: {}".format(
        first_name,
        ", ".join(item_bits),
        req.estimatedDeliveryDays,
        _format_dollars(req.grandTotalCents),
    )

    record = NotificationRecord(
        notificationId=notification_id,
        orderId=req.orderId,
        channel="email",
        status="sent",
        subject="Your VoltRide order {} is confirmed!".format(req.orderId),
        previewText=preview,
        sentAt=datetime.now(timezone.utc).isoformat(),
    )
    _notifications[notification_id] = record

    return {
        "notificationId": record.notificationId,
        "channel": record.channel,
        "status": record.status,
        "subject": record.subject,
        "previewText": record.previewText,
    }


@app.get("/api/notifications")
def list_notifications(orderId: str = ""):
    records = [
        n for n in _notifications.values()
        if not orderId or n.orderId == orderId
    ]
    return {"notifications": records}

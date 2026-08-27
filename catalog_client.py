"""HTTP client for the catalog service.

Notifications keeps its own local view of catalog's /summary contract;
it only needs the product name to render email copy.
"""
import os
from typing import Optional

import httpx

CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:4001")


async def get_product_name(product_id: str) -> Optional[str]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{CATALOG_URL}/api/products/{product_id}/summary")
    if resp.status_code != 200:
        return None
    return resp.json().get("name")

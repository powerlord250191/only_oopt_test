import unittest
from decimal import Decimal
from unittest.mock import AsyncMock

from starter import recommend_price


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_uses_eligible_competitor_and_rounds_down(self):
        fetch_offers = AsyncMock(return_value={
            "status": "success",
            "offers": [
                {"seller": "MyShOp", "price": Decimal("4300.00"), "delivery_days": 2},
                {"seller": "UNKNOWN", "price": Decimal("4400.00"), "delivery_days": None},
                {"seller": "SLOW", "price": Decimal("4700.00"), "delivery_days": 7},
                {"seller": "PARTS", "price": Decimal("4800.11"), "delivery_days": 6},
            ],
        })

        result = await recommend_price(fetch_offers, Decimal("4900.00"), Decimal("4500.00"))

        self.assertEqual(result["decision"], "APPLY")
        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal("4728.10"))

    async def test_holds_current_price_when_source_returns_partial_data(self):
        fetch_offers = AsyncMock(return_value={
            "status": "partial",
            "offers": [
                {"seller": "PARTS", "price": Decimal("4800.00"), "delivery_days": 3},
            ],
        })

        result = await recommend_price(fetch_offers, Decimal("4400.00"), Decimal("4500.00"))

        self.assertEqual(result["decision"], "HOLD")
        self.assertEqual(result["price"], Decimal("4400.00"))

import json
import sys
import unittest
from decimal import Decimal
from types import ModuleType
from unittest.mock import AsyncMock, patch

try:
    import redis.asyncio
except ModuleNotFoundError:
    redis_module = ModuleType("redis")
    redis_asyncio_module = ModuleType("redis.asyncio")
    redis_asyncio_module.Redis = type(
        "Redis", (), {"from_url": staticmethod(lambda *args, **kwargs: None)}
    )
    redis_module.asyncio = redis_asyncio_module
    sys.modules["redis"] = redis_module
    sys.modules["redis.asyncio"] = redis_asyncio_module

from app.services.cache import get_revenue_summary
from app.services.reservations import format_currency_amount, get_month_bounds_utc


class RevenueCacheTests(unittest.IsolatedAsyncioTestCase):
    async def test_uses_a_distinct_cache_key_for_each_tenant(self):
        redis_client = type("RedisClient", (), {})()
        redis_client.get = AsyncMock(return_value=None)
        redis_client.setex = AsyncMock()
        revenue = {
            "property_id": "prop-001",
            "tenant_id": "tenant-a",
            "total": "1000.00",
            "currency": "USD",
            "count": 3,
        }

        with (
            patch("app.services.cache.redis_client", redis_client),
            patch(
                "app.services.reservations.calculate_total_revenue",
                AsyncMock(return_value=revenue),
            ),
        ):
            await get_revenue_summary("prop-001", "tenant-a")

        redis_client.get.assert_awaited_once_with("revenue:tenant-a:prop-001")
        redis_client.setex.assert_awaited_once_with(
            "revenue:tenant-a:prop-001", 300, json.dumps(revenue)
        )


class RevenueCalculationTests(unittest.TestCase):
    def test_month_bounds_follow_the_property_timezone(self):
        start_date, end_date = get_month_bounds_utc(2024, 3, "Europe/Paris")

        self.assertEqual(start_date.isoformat(), "2024-02-29T23:00:00+00:00")
        self.assertEqual(end_date.isoformat(), "2024-03-31T22:00:00+00:00")

    def test_currency_amount_rounds_once_with_decimal_precision(self):
        self.assertEqual(format_currency_amount(Decimal("1000.005")), "1000.01")
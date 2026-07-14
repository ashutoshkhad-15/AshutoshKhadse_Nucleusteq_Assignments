from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core import seed


@pytest.mark.asyncio
async def test_run_seed_inserts_admin_when_missing():
    fake_collection = MagicMock()
    fake_collection.find_one = AsyncMock(return_value=None)
    fake_collection.insert_one = AsyncMock()
    fake_db = {"users": fake_collection}

    with patch.object(seed, "connect_to_mongo", AsyncMock()), \
         patch.object(seed, "close_mongo_connection", AsyncMock()), \
         patch.object(seed, "get_database", return_value=fake_db), \
         patch.object(seed, "encode_password", return_value="encoded"), \
         patch.object(seed.settings, "DEFAULT_ADMIN_PASSWORD", "secret"):
        await seed.run_seed()

    fake_collection.insert_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_seed_skips_existing_admin():
    fake_collection = MagicMock()
    fake_collection.find_one = AsyncMock(return_value={"email": "admin@nucleusteq.com"})
    fake_collection.insert_one = AsyncMock()
    fake_db = {"users": fake_collection}

    with patch.object(seed, "connect_to_mongo", AsyncMock()), \
         patch.object(seed, "close_mongo_connection", AsyncMock()), \
         patch.object(seed, "get_database", return_value=fake_db):
        await seed.run_seed()

    fake_collection.insert_one.assert_not_awaited()


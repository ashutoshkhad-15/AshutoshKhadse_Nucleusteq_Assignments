from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.database import close_mongo_connection, connect_to_mongo, db_config, get_database


@pytest.mark.asyncio
async def test_connect_to_mongo_sets_client_and_db():
    fake_client = MagicMock()
    fake_client.admin.command = AsyncMock(return_value={"ok": 1})
    fake_client.__getitem__.return_value = {"name": "db"}

    with patch("src.core.database.AsyncIOMotorClient", return_value=fake_client):
        await connect_to_mongo()

    assert db_config.client is fake_client
    assert db_config.db == {"name": "db"}


@pytest.mark.asyncio
async def test_close_mongo_connection_closes_client():
    fake_client = MagicMock()
    db_config.client = fake_client

    await close_mongo_connection()

    fake_client.close.assert_called_once()


def test_get_database_returns_configured_db():
    db_config.db = {"name": "db"}
    assert get_database() == {"name": "db"}


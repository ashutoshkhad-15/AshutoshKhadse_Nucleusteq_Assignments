"""Repository tests for user persistence workflows."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.user_repository import UserRepository


@pytest.fixture
def user_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {"users": MagicMock(), "interviews": MagicMock()}[key]
    with patch("src.repositories.user_repository.get_database", return_value=db):
        repo = UserRepository()
        repo.collection.find_one = AsyncMock()
        repo.collection.insert_one = AsyncMock()
        repo.collection.update_one = AsyncMock()
        repo.collection.count_documents = AsyncMock()
        repo.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value.to_list = AsyncMock(return_value=[])
        yield repo


@pytest.mark.asyncio
class TestUserRepository:
    async def test_create_and_get_user(self, user_repository):
        user_repository.collection.insert_one.return_value = MagicMock(inserted_id="user1")
        created = await user_repository.create_user({"email": "a@nucleusteq.com"})
        assert created["_id"] == "user1"

        user_repository.collection.find_one.return_value = {"_id": MagicMock(), "email": "a@nucleusteq.com"}
        found = await user_repository.get_user_by_email("a@nucleusteq.com")
        assert found["email"] == "a@nucleusteq.com"

    async def test_get_all_and_search_users(self, user_repository):
        user_repository.collection.count_documents.return_value = 1
        user_repository.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value.to_list = AsyncMock(
            return_value=[{"_id": MagicMock(), "email": "a@nucleusteq.com"}]
        )
        users, total = await user_repository.get_all_users()
        assert total == 1 and users[0]["email"] == "a@nucleusteq.com"

        users, total = await user_repository.search_users("hr")
        assert total == 1 and users[0]["email"] == "a@nucleusteq.com"

    async def test_get_user_by_id_invalid_and_valid(self, user_repository):
        user_repository.collection.find_one.return_value = {"_id": MagicMock(), "email": "a@nucleusteq.com"}
        assert (await user_repository.get_user_by_id("507f1f77bcf86cd799439011"))["email"] == "a@nucleusteq.com"
        assert await user_repository.get_user_by_id("bad-id") is None

    async def test_update_and_default_admin(self, user_repository):
        await user_repository.update_user("a@nucleusteq.com", {"name": "A"})
        user_repository.collection.update_one.assert_awaited()

        user_repository.collection.find_one.return_value = {"_id": MagicMock(), "email": "admin@nucleusteq.com"}
        assert (await user_repository.get_default_admin())["email"] == "admin@nucleusteq.com"

    async def test_repository_error_wraps_as_app_exception(self, user_repository):
        user_repository.collection.find_one.side_effect = Exception("boom")
        with pytest.raises(AppBaseException):
            await user_repository.get_user_by_email("x@nucleusteq.com")

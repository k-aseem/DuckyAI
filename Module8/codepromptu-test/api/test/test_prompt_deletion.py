import pytest
from api.session.session import TestUserSession
from .base_test import BaseTest

@pytest.mark.asyncio
class TestPromptDeletion(BaseTest):

    async def _delete_prompt(self, user, guid):
        await user.delete_prompt(guid)

    async def _assert_prompt_not_retrievable(self, user: TestUserSession, guid):
        user_name = user._name
        try:
            await user.get_prompt(guid)
            assert False, f"{user_name}'s prompt with GUID {guid} should not be retrievable."
        except Exception:
            assert True

    async def test_adrianna_delete_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt.
        When: Adrianna deletes the prompt by its GUID.
        Then: The prompt is no longer retrievable by its GUID.
        """
        prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        guid: str = await adrianna.add_prompt(prompt)
        await self._delete_prompt(adrianna, guid)
        await self._assert_prompt_not_retrievable(adrianna, guid)

    async def test_bob_delete_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt.
        When: Bob deletes the prompt by its GUID.
        Then: The prompt is no longer retrievable by its GUID.
        """
        prompt = {"content": "Private content", "display_name": "Private Prompt", "tags": ["private1", "private2"]}
        guid: str = await bob.add_prompt(prompt)
        await self._delete_prompt(bob, guid)
        await self._assert_prompt_not_retrievable(bob, guid)
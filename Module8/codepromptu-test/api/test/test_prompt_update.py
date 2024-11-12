import pytest
from api.session.session import TestUserSession
from .base_test import BaseTest

@pytest.mark.asyncio
class TestPromptUpdate(BaseTest):

    async def _get_prompt(self, user, created_guid):
        retrieved_prompt = await user.get_prompt(created_guid)
        return retrieved_prompt

    async def _assert_prompts_equal(self, user: TestUserSession, expected_guid, expected_prompt, actual_prompt):
        user_name = user._name
        assert actual_prompt[
                   'guid'] == expected_guid, f"{user_name}'s retrieved prompt GUID does not match the created prompt's GUID."
        assert actual_prompt['content'] == expected_prompt[
            'content'], f"The content of {user_name}'s retrieved prompt does not match the expected content."
        assert actual_prompt['display_name'] == expected_prompt[
            'display_name'], f"The display name of {user_name}'s retrieved prompt does not match the expected display name."
        assert set(actual_prompt['tags']) == set(
            expected_prompt['tags']), f"The tags of {user_name}'s retrieved prompt do not match the expected tags."

    async def test_adrianna_update_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt and updates its content, display name, and tags.
        When: Adrianna retrieves the updated prompt by its GUID.
        Then: The retrieved prompt matches the updated content, display name, and tags.
        """
        initial_prompt = {"content": "Initial content", "display_name": "Initial Prompt", "tags": ["tag1", "tag2"]}
        updated_prompt = {"content": "Updated content", "display_name": "Updated Prompt", "tags": ["tag3", "tag4"]}
        prompt_guid: str = await adrianna.add_prompt(initial_prompt)
        await adrianna.update_prompt(prompt_guid, updated_prompt)
        actual_prompt = await self._get_prompt(adrianna, prompt_guid)

        await self._assert_prompts_equal(adrianna, prompt_guid, updated_prompt, actual_prompt)

    async def test_bob_update_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt and updates its content, display name, and tags.
        When: Bob retrieves the updated prompt by its GUID.
        Then: The retrieved prompt matches the updated content, display name, and tags.
        """
        initial_prompt = {"content": "Initial private content", "display_name": "Initial Private Prompt", "tags": ["private1", "private2"]}
        updated_prompt = {"content": "Updated private content", "display_name": "Updated Private Prompt", "tags": ["private3", "private4"]}
        prompt_guid: str = await bob.add_prompt(initial_prompt)
        await bob.update_prompt(prompt_guid, updated_prompt)
        actual_prompt = await self._get_prompt(bob, prompt_guid)

        await self._assert_prompts_equal(bob, prompt_guid, updated_prompt, actual_prompt)
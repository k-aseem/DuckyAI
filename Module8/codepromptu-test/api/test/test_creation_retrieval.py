import pytest

from api.session.session import TestUserSession
from .base_test import BaseTest


@pytest.mark.asyncio
class TestPromptCreationRetrieval(BaseTest):

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

    async def test_adrianna_create_retrieve_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt with specific content, display name, and tags.
        When: Adrianna retrieves the prompt by its GUID.
        Then: The retrieved prompt's GUID matches the created one, and the content, display name, and tags match as well.
        """
        expected_prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        expected_guid: str = await adrianna.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(adrianna, expected_guid)

        await self._assert_prompts_equal(adrianna, expected_guid, expected_prompt, actual_prompt)


    async def test_bob_create_retrieve_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt with specific content, display name, and tags.
        When: Bob retrieves the prompt by its GUID.
        Then: The retrieved prompt's GUID matches the created one, and the content, display name, and tags match as well.
        """
        expected_prompt = {"content": "Private content", "display_name": "Private Prompt", "tags": ["private1", "private2"]}
        expected_guid = await bob.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(bob, expected_guid)
        await self._assert_prompts_equal(bob, expected_guid, expected_prompt, actual_prompt)
        
    async def test_alice_retrieve_adrianna_public_prompt(self, adrianna, alice):
        """
        Given: Adrianna creates a public prompt with specific content, display name, and tags.
        When: Alice retrieves the prompt by its GUID.
        Then: The retrieved prompt's GUID matches the created one, and the content, display name, and tags match as well.
        """
        expected_prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        expected_guid: str = await adrianna.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(alice, expected_guid)
        await self._assert_prompts_equal(alice, expected_guid, expected_prompt, actual_prompt)

    async def test_alice_failing_to_create_prompt(self, alice):
        """
        Given: Alice attempts to create a prompt with specific content, display name, and tags.
        When: The system processes Alice's request to create the prompt.
        Then: The system returns an error indicating that the prompt creation failed due to lack of permissions.
        """
        prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        
        try:
            await alice.add_prompt(prompt)
            assert False, "Alice's prompt creation should have failed due to lack of permissions, but it succeeded."
        except Exception as e:
            assert "not authenticated" in str(e).lower(), f"Unexpected error message: {str(e)}"

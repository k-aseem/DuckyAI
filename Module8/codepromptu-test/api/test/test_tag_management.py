import pytest
from api.session.session import TestUserSession
from .base_test import BaseTest

@pytest.mark.asyncio
class TestTagManagement(BaseTest):

    async def _get_prompt(self, user, created_guid):
        retrieved_prompt = await user.get_prompt(created_guid)
        return retrieved_prompt

    async def _assert_tags_equal(self, user: TestUserSession, expected_tags, actual_tags):
        user_name = user._name
        assert set(actual_tags) == set(expected_tags), f"The tags of {user_name}'s retrieved prompt do not match the expected tags."

    async def test_adrianna_add_tag_to_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt.
        When: Adrianna adds a new tag to the prompt.
        Then: The prompt's tags include the new tag.
        """
        initial_prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        new_tag = "new_tag"
        expected_tags = initial_prompt["tags"] + [new_tag]

        prompt_guid = await adrianna.add_prompt(initial_prompt)
        await adrianna.add_tag_to_prompt(prompt_guid, new_tag)
        actual_prompt = await self._get_prompt(adrianna, prompt_guid)

        await self._assert_tags_equal(adrianna, expected_tags, actual_prompt['tags'])

    async def test_adrianna_remove_tag_from_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt with multiple tags.
        When: Adrianna removes one of the tags from the prompt.
        Then: The prompt's tags no longer include the removed tag.
        """
        initial_prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        tag_to_remove = "tag1"
        expected_tags = [tag for tag in initial_prompt["tags"] if tag != tag_to_remove]

        prompt_guid = await adrianna.add_prompt(initial_prompt)
        await adrianna.remove_tag_from_prompt(prompt_guid, tag_to_remove)
        actual_prompt = await self._get_prompt(adrianna, prompt_guid)

        await self._assert_tags_equal(adrianna, expected_tags, actual_prompt['tags'])

    async def test_bob_add_tag_to_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt.
        When: Bob adds a new tag to the prompt.
        Then: The prompt's tags include the new tag.
        """
        initial_prompt = {"content": "Private content", "display_name": "Private Prompt", "tags": ["private1", "private2"]}
        new_tag = "new_private_tag"
        expected_tags = initial_prompt["tags"] + [new_tag]

        prompt_guid = await bob.add_prompt(initial_prompt)
        await bob.add_tag_to_prompt(prompt_guid, new_tag)
        actual_prompt = await self._get_prompt(bob, prompt_guid)

        await self._assert_tags_equal(bob, expected_tags, actual_prompt['tags'])

    async def test_bob_remove_tag_from_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt with multiple tags.
        When: Bob removes one of the tags from the prompt.
        Then: The prompt's tags no longer include the removed tag.
        """
        initial_prompt = {"content": "Private content", "display_name": "Private Prompt", "tags": ["private1", "private2"]}
        tag_to_remove = "private1"
        expected_tags = [tag for tag in initial_prompt["tags"] if tag != tag_to_remove]

        prompt_guid = await bob.add_prompt(initial_prompt)
        await bob.remove_tag_from_prompt(prompt_guid, tag_to_remove)
        actual_prompt = await self._get_prompt(bob, prompt_guid)

        await self._assert_tags_equal(bob, expected_tags, actual_prompt['tags'])

    async def test_add_duplicate_tag_to_prompt(self, adrianna):
        """
        Given: A user creates a prompt and attempts to add a duplicate tag.
        When: The user submits the request to add the duplicate tag.
        Then: The system prevents the addition of the duplicate tag and returns an appropriate error message.
        """
        initial_prompt = {"content": "Test content", "display_name": "Test Prompt", "tags": ["tag1", "tag2"]}
        duplicate_tag = "tag1"
        expected_tags = initial_prompt["tags"]

        prompt_guid = await adrianna.add_prompt(initial_prompt)
        with pytest.raises(Exception) as excinfo:
            await adrianna.add_tag_to_prompt(prompt_guid, duplicate_tag)
        assert "an unexpected error occurred while processing your request." in str(excinfo.value).lower()

        actual_prompt = await self._get_prompt(adrianna, prompt_guid)
        await self._assert_tags_equal(adrianna, expected_tags, actual_prompt['tags'])
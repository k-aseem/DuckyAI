### Test Group: Prompt Creation and Retrieval

1. **Test Case: Creating and Retrieving a Public Prompt by Adrianna**

    - **Given**: Adrianna creates a public prompt with specific content, display name, and tags.
    - **When**: Adrianna retrieves the prompt by its GUID.
    - **Then**: The retrieved prompt matches the created one in content, display name, and tags.

2. **Test Case: Creating and Retrieving a Private Prompt by Bob**

    - **Given**: Bob creates a private prompt with specific content, display name, and tags.
    - **When**: Bob retrieves the prompt by its GUID.
    - **Then**: The retrieved prompt matches the created one in content, display name, and tags.

3. **Test Case: Retrieving a Public Prompt by Alice**

    - **Given**: Adrianna creates a public prompt.
    - **When**: Alice retrieves the prompt by its GUID.
    - **Then**: The retrieved prompt matches the created one in content, display name, and tags.

4. **Test Case: Retrieving a Non-Existent Prompt**

    - **Given**: No prompt exists with a specific GUID.
    - **When**: A user attempts to retrieve the prompt by its GUID.
    - **Then**: The system returns an error indicating the prompt does not exist.

5. **Test Case: Failing to Create a Prompt by Alice**

    - **Given**: Alice attempts to create a prompt with specific content, display name, and tags.
    - **When**: The system processes Alice's request to create the prompt.
    - **Then**: The system returns an error indicating that the prompt creation failed.

### Test Group: Prompt Update

1. **Test Case: Updating a Public Prompt by Adrianna**

    - **Given**: Adrianna creates a public prompt and updates its content, display name, and tags.
    - **When**: Adrianna retrieves the updated prompt by its GUID.
    - **Then**: The retrieved prompt matches the updated content, display name, and tags.

2. **Test Case: Updating a Private Prompt by Bob**
    - **Given**: Bob creates a private prompt and updates its content, display name, and tags.
    - **When**: Bob retrieves the updated prompt by its GUID.
    - **Then**: The retrieved prompt matches the updated content, display name, and tags.

### Test Group: Prompt Deletion

1. **Test Case: Deleting a Public Prompt by Adrianna**

    - **Given**: Adrianna creates a public prompt.
    - **When**: Adrianna deletes the prompt by its GUID.
    - **Then**: The prompt is no longer retrievable by its GUID.

2. **Test Case: Deleting a Private Prompt by Bob**
    - **Given**: Bob creates a private prompt.
    - **When**: Bob deletes the prompt by its GUID.
    - **Then**: The prompt is no longer retrievable by its GUID.

### Test Group: Tag Management

1. **Test Case: Adding a Tag to a Public Prompt by Adrianna**

    - **Given**: Adrianna creates a public prompt.
    - **When**: Adrianna adds a new tag to the prompt.
    - **Then**: The prompt's tags include the new tag.

2. **Test Case: Removing a Tag from a Public Prompt by Adrianna**

    - **Given**: Adrianna creates a public prompt with multiple tags.
    - **When**: Adrianna removes one of the tags from the prompt.
    - **Then**: The prompt's tags no longer include the removed tag.

3. **Test Case: Adding a Tag to a Private Prompt by Bob**

    - **Given**: Bob creates a private prompt.
    - **When**: Bob adds a new tag to the prompt.
    - **Then**: The prompt's tags include the new tag.

4. **Test Case: Removing a Tag from a Private Prompt by Bob**

    - **Given**: Bob creates a private prompt with multiple tags.
    - **When**: Bob removes one of the tags from the prompt.
    - **Then**: The prompt's tags no longer include the removed tag.

5. **Test Case: Adding Duplicate Tags to a Prompt**
    - **Given**: A user creates a prompt and attempts to add a duplicate tag.
    - **When**: The user submits the request to add the duplicate tag.
    - **Then**: The system prevents the addition of the duplicate tag and returns an appropriate error message.

import os
from datetime import datetime
from typing import Literal, Tuple
from urllib.parse import urlparse

import httpx
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

__IMAGES_BASE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/images')


def get_all_images() -> pd.DataFrame:
    """
    Retrieves a DataFrame containing information about all images stored in a folder.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Image', 'Description', and 'Date Created',
                      where 'Image' is the file path, 'Description' is the associated
                      description, and 'Date Created' is the creation timestamp.

    # AI Generation Prompt:
    # Write a Python function that reads all `.png` image files from a given folder, retrieves
    # their associated descriptions from a `.txt` file with the same name, and returns a pandas
    # DataFrame containing the image file paths, descriptions, and creation timestamps.
    """
    image_data = []
    for filename in os.listdir(__IMAGES_BASE_FOLDER):
        if filename.endswith('.png'):
            image_path = os.path.join(__IMAGES_BASE_FOLDER, filename)
            description_path = os.path.splitext(image_path)[0] + '.txt'
            if os.path.exists(description_path):
                with open(description_path, 'r') as file:
                    description = file.read().strip()
            else:
                description = ''
            creation_time = datetime.fromtimestamp(os.path.getctime(image_path))
            image_data.append({
                'image_path': image_path,
                'description': description,
                'date_created': creation_time
            })
    return pd.DataFrame(image_data)


def delete_image(image_path: str):
    """
    Deletes an image file and its associated description file (if it exists).

    Args:
        image_path (str): The path to the image file to be deleted.

    # AI Generation Prompt:
    # Write a Python function that deletes a given image file and its corresponding `.txt`
    # description file, if the description file exists.
    """
    if os.path.exists(image_path):
        os.remove(image_path)
    description_path = os.path.splitext(image_path)[0] + '.txt'
    if os.path.exists(description_path):
        os.remove(description_path)


async def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    style: Literal["vivid", "natural"] = "vivid",
    quality: Literal["standard", "hd"] = "hd",
    timeout: int = 100,
    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024"
) -> Tuple[str, str]:
    """
    Generates an image based on a given text prompt using the OpenAI DALL-E model
    and saves the image to a local folder.

    Args:
        prompt (str): The description or prompt for generating the image.
        model (str): The model version to use (default is "dall-e-3").
        style (Literal): The style of the image, e.g., "vivid" or "natural".
        quality (Literal): The quality setting, either "standard" or "hd".
        timeout (int): The maximum time (in seconds) to wait for the image to be generated.
        size (Literal): The size of the image, e.g., "1024x1024", "1792x1024", etc.

    Returns:
        Tuple[str, str]: A tuple containing the prompt and the file path of the saved image.

    # AI Generation Prompt:
    # Write a Python asynchronous function that generates an image from a text prompt using the
    # OpenAI DALL-E model, retrieves the image from the resulting URL, and saves it locally in
    # a predefined folder. The function should also save the prompt in a `.txt` file alongside
    # the image.
    """
    client = OpenAI(base_url='http://aitools.cs.vt.edu:7860/openai/v1', api_key='aitools')
    async with httpx.AsyncClient(timeout=timeout) as http_client:
        response = await http_client.post(
            str(client.base_url) + "/images/generations",
            headers={"Authorization": f"Bearer {client.api_key}"},
            json={
                "model": model,
                "prompt": prompt,
                "style": style,
                "quality": quality,
                "size": size
            }
        )
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]

        # Download the image
        image_response = await http_client.get(image_url)
        image_response.raise_for_status()

        # Save the image
        filename = extract_filename_from_url(image_url)
        image_path = os.path.join(__IMAGES_BASE_FOLDER, filename)
        with open(image_path, "wb") as image_file:
            image_file.write(image_response.content)

        # Save the prompt in a .txt file
        description_path = os.path.splitext(image_path)[0] + '.txt'
        with open(description_path, "w") as description_file:
            description_file.write(prompt)

    return image_path


def extract_filename_from_url(url: str) -> str:
    """
    Extracts the filename from a given URL.

    Args:
        url (str): The URL from which to extract the filename.

    Returns:
        str: The extracted filename.

    # AI Generation Prompt:
    # Write a Python function that takes a URL as input, extracts the file path, and returns
    # the filename from the URL.
    """
    # Parse the URL into components
    url_path = urlparse(url).path

    # Extract the filename from the path
    filename = os.path.basename(url_path)

    return filename
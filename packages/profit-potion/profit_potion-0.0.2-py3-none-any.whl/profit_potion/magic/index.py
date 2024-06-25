"""
This is the main module to make magic
"""

import os
import base64
from openai import OpenAI


# pylint: disable=too-few-public-methods
class Analyst:
    """
    This is the class Analyst to make magic
    """

    def __init__(self, token: str):
        """
        This is the constructor for the Analyst class
        """
        os.environ["OPENAI_API_KEY"] = token

        # Check if openai api key is set
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OpenAI API key is not set")

        self.client = OpenAI()

    def encoding_images(self, images_list: list) -> list:
        """
        This is the method to encode images in bs64 and return a list of strings
        """
        encoded_images = []
        for image in images_list:
            with open(image, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                image_element = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"},
                }

                encoded_images.append(image_element)

        return encoded_images

    def analyze_data(
        self,
        images_list: list = None,
        prompt: str = None,
        max_tokens: int = 300,
        model: str = "gpt-4o",
    ):
        """
        This is the method to analyze data
        """
        content = [
            {"type": "text", "text": prompt},
        ]

        if images_list:
            encoded_images = self.encoding_images(images_list)
            content.extend(encoded_images)

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
        )

        return response.choices[0]

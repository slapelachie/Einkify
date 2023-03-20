"""
image_processor.py
author: slapelachie <slapelachie@gmail.com>
"""
import os
from typing import Dict, List

from PIL import Image

from ..constants import MAX_DIMENSION, ZOOM_FACTOR


def has_allowed_extension(
    image_path: str, allowed_extensions: List[str]
) -> bool:
    """
    Check if an image file has an allowed extension.

    Args:
        image_path (str): The path to the image file to check.
        allowed_extensions (List[str]): A list of allowed extensions.

    Returns:
        bool: True if the image has an allowed extension, False otherwise.

    Example:
        >>> has_allowed_extension("image.jpg", [".jpg", ".png"])
        True
        >>> has_allowed_extension("image.bmp", [".jpg", ".png"])
        False
    """
    if not image_path:
        raise ValueError("Please specify an image path")
    _, extension = os.path.splitext(image_path)
    return extension.lower() in allowed_extensions


def get_image_paths(image_directory: str) -> List[str]:
    """
    Get a list of relative image file paths in the given directory.

    Args:
        image_directory: A string representing the path to the directory containing the images.

    Returns:
        A list of relative image file paths with allowed extensions in the directory.
    """
    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".tiff",
        ".webp",
    ]

    if not os.path.exists(image_directory):
        raise FileNotFoundError("Specified image_directory does not exist")

    image_paths = []
    for root, _, files in os.walk(image_directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, image_directory)
            if has_allowed_extension(relative_path, allowed_extensions):
                image_paths.append(relative_path)

    return image_paths


def convert_image(image: Image, profile: Dict) -> Image:
    """
    Converts the input image based on the provided profile.

    Args:
        image (PIL.Image): The input image to convert.
        profile (dict): The conversion profile.

    Returns:
        PIL.Image: The converted image.
    """
    if profile.get("mono"):
        image = image.convert("L")

    max_dimension = profile.get("max_dimension", MAX_DIMENSION) * profile.get(
        "zoom_factor", ZOOM_FACTOR
    )
    image.thumbnail((max_dimension, max_dimension), resample=Image.LANCZOS)

    return image


def save_image(
    image: Image, output_directory: str, image_path: str, image_type: str
) -> None:
    """
    Saves the given image with the specified type to the output directory.

    Args:
        image: The image to save.
        output_directory: The directory to save the image to.
        image_path: The relative path of the image within the input directory.
        image_type: The type of the image to save (e.g. 'jpg', 'png').

    Returns:
        None.
    """
    image_out_path = os.path.join(output_directory, image_path)
    os.makedirs(os.path.dirname(image_out_path), exist_ok=True)
    image.save(
        f"{os.path.splitext(os.path.join(output_directory, image_path))[0]}.{image_type}",
        format=image_type,
    )


def process_images(profile: Dict, image_directory: str) -> str:
    """
    Processes images in a given directory according to a given profile.

    Args:
    - profile (dict): A dictionary containing the parameters of the image processing profile.
    - image_directory (str): The directory containing the images to be processed.

    Returns:
    - output_directory (str): The directory containing the processed images.
    """
    output_directory = os.path.join(os.path.dirname(image_directory), "convert")
    image_paths = get_image_paths(image_directory)

    for image_path in image_paths:
        image = Image.open(os.path.join(image_directory, image_path))
        image = convert_image(image, profile)
        image_type = profile.get("type", "jpg")
        save_image(image, output_directory, image_path, image_type)

    return output_directory

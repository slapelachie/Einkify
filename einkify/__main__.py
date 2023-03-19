import argparse
import os
import tempfile
import zipfile
import rarfile
import yaml
from typing import Dict
from PIL import Image

MAX_DIMENSION = 100000
ZOOM_FACTOR = 2
DEFAULT_PROFILE = {
    "mono": False,
    "type": "jpg",
    "max_width": MAX_DIMENSION,
    "max_height": MAX_DIMENSION,
    "zoom_factor": ZOOM_FACTOR,
}


class VerifyFileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"


def parse_arguments() -> argparse.Namespace:
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Program to convert manga into a kobo compatible format."
    )

    # Define the arguments
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument(
        "-i", "--input", dest="input_file", type=str, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-o", "--output", dest="output_file", type=str, help="Path to the output file"
    )
    parser.add_argument("--profile", type=str, help="Profile to use")
    parser.add_argument(
        "--manga", action="store_true", help="If epub should be in rtl format"
    )

    # Parse the arguments
    return parser.parse_args()


def extract_file(file_path: str, temp_directory: str) -> str:
    allowed_extensions = ["cbz", "cbr"]

    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        raise FileNotFoundError("The file does not exist")

    file_name, extension = os.path.splitext(os.path.basename(file_path))
    extension = extension[1:].lower()
    if extension not in allowed_extensions:
        raise VerifyFileError("File is not a cbz or cbr file")

    extract_directory = os.path.join(temp_directory, file_name)

    if extension in ["cbz", "zip"]:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_directory)
    elif extension in ["cbr", "rar"]:
        with rarfile.RarFile(file_path, "r") as rar_ref:
            rar_ref.extractall(extract_directory)
    else:
        raise ValueError("Unsupported archive type")

    return extract_directory


def process_profile(profile: Dict, profile_path: str):
    if not (os.path.exists(profile_path) and os.path.isfile(profile_path)):
        raise VerifyFileError("Given file is not a valid profile file")

    data = {}
    with open(profile_path, "r") as stream:
        data = yaml.safe_load(stream)

    profile = DEFAULT_PROFILE.copy()
    profile.update(data)

    return profile


def process_images(profile: Dict, image_directory: str) -> str:
    allowed_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"]
    output_directory = os.path.join(os.path.dirname(image_directory), "convert")

    image_paths = []
    for root, directories, files in os.walk(image_directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, image_directory)
            image_paths.append(relative_path)

    for image_path in image_paths:
        image = Image.open(os.path.join(image_directory, image_path))

        if profile.get("mono"):
            image = image.convert("L")

        image_out_path = os.path.join(output_directory, image_path)
        os.makedirs(os.path.dirname(image_out_path), exist_ok=True)

        max_dimension = profile.get("max_dimension", MAX_DIMENSION) * profile.get(
            "zoom_factor", ZOOM_FACTOR
        )
        image.thumbnail((max_dimension, max_dimension), resample=Image.LANCZOS)

        image_type = profile.get("type", "jpg")
        image.save(
            f"{os.path.splitext(os.path.join(output_directory, image_path))[0]}.{image_type}",
            format=image_type,
        )


if __name__ == "__main__":
    arguments = parse_arguments()

    temp_directory = tempfile.TemporaryDirectory()
    extract_directory = extract_file(arguments.input_file, temp_directory.name)

    profile = DEFAULT_PROFILE.copy()
    if arguments.profile:
        profile = process_profile(profile, arguments.profile)

    process_images(profile, extract_directory)

    input()

    # temp_directory.cleanup()

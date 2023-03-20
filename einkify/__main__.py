"""
main.py
author: slapelachie <slapelachie@gmail.com>
"""
import os
import tempfile


from .cli import parse_arguments
from .archive_extractor import extract_file
from .profile_processor import get_profile
from .image_processor import process_images
from .ebook_generator import make_ebook


def get_title(input_file: str) -> str:
    return os.path.splitext(os.path.basename(input_file))[0]


def main() -> None:
    """
    Main function that executes the program.

    Returns:
        None
    """
    arguments = parse_arguments()

    temp_directory = tempfile.TemporaryDirectory()
    title = get_title(arguments.input_file)
    extract_directory = extract_file(arguments.input_file, temp_directory.name)

    profile = get_profile(arguments.profile)
    processed_images_directory = process_images(profile, extract_directory)

    # TODO: Check output exists
    make_ebook(title, processed_images_directory, arguments.output_file)
    input("Press any key to quit...")


if __name__ == "__main__":
    main()

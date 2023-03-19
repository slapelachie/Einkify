"""
main.py
author: slapelachie <slapelachie@gmail.com>
"""
import tempfile


from .cli import parse_arguments
from .archive import extract_file
from .profile import get_profile
from .image import process_images


def main() -> None:
    """
    Main function that executes the program.

    Returns:
        None
    """
    arguments = parse_arguments()

    temp_directory = tempfile.TemporaryDirectory()
    extract_directory = extract_file(arguments.input_file, temp_directory.name)

    profile = get_profile(arguments.profile)
    process_images(profile, extract_directory)
    input("Press any key to quit...")


if __name__ == "__main__":
    main()

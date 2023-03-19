"""
archive_extractor.py
author: slapelachie <slapelachie@gmail.com>
"""
import os
import zipfile
import rarfile

from ..error import VerifyFileError


def extract_file(file_path: str, temp_directory: str) -> str:
    """
    Extracts a comic book archive file (.cbz, .cbr) to a temporary directory.

    Args:
        file_path (str): The path to the comic book archive file to extract.
        temp_directory (str): The path to the temporary directory to extract the file to.

    Returns:
        str: The path to the directory containing the extracted files.
    """
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

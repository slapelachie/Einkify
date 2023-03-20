"""
profile_processor.py
author: slapelachie <slapelachie@gmail.com>
"""
import os
from typing import Dict, Optional

import yaml

from .constants import MAX_DIMENSION, ZOOM_FACTOR
from .error import VerifyFileError

DEFAULT_PROFILE = {
    "mono": False,
    "type": "jpg",
    "max_width": MAX_DIMENSION,
    "max_height": MAX_DIMENSION,
    "zoom_factor": ZOOM_FACTOR,
}


def process_profile(profile: Dict, profile_path: str) -> Dict:
    """
    Load and process the given profile file.

    Args:
    - profile: A dictionary containing default profile configuration.
    - profile_path: A string representing the path to the profile file.

    Returns:
    - A dictionary with the updated profile configuration after merging with the
      contents of the profile file.

    Raises:
    - VerifyFileError: If the given file path is not valid or the file does not exist.
    """
    if not (os.path.exists(profile_path) and os.path.isfile(profile_path)):
        raise VerifyFileError("Given file is not a valid profile file")

    data = {}
    with open(profile_path, "r", encoding="UTF-8") as stream:
        data = yaml.safe_load(stream)

    profile = DEFAULT_PROFILE.copy()
    profile.update(data)

    return profile


def get_profile(profile_path: Optional[str] = None) -> Dict:
    """
    Loads a profile from a file and returns the profile as a dictionary.

    Args:
        profile_path (str, optional): A file path to the profile file. Defaults to None.

    Returns:
        dict: A dictionary containing the profile information.
    """
    profile = DEFAULT_PROFILE.copy()
    if profile_path:
        profile = process_profile(profile, profile_path)

    return profile

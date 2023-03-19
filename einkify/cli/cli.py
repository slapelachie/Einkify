"""
cli.py
author: slapelachie <slapelachie@gmail.com>
"""
import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Parses the command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
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
        "-o",
        "--output",
        dest="output_file",
        type=str,
        help="Path to the output file",
    )
    parser.add_argument("--profile", type=str, help="Profile to use")
    parser.add_argument(
        "--manga", action="store_true", help="If epub should be in rtl format"
    )

    # Parse the arguments
    return parser.parse_args()

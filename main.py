#!/usr/bin/python
#
# References:
# https://pypdf2.readthedocs.io
# https://github.com/mstamy2/PyPDF2

from typing import List, Tuple

from utilities import check_pre_reqs, clear_directory, clear_screen, get_file_to_split, ghost_export, has_arg, split_pdf, welcome_screen

# Global Variables
#

INPUT_DIR = './input'
TEMP_DIR = './temp'
OUTPUT_DIR = './output'

"""
Each tuple is a pair of coordinates in this format:
[
  (lower_left_x, lower_left_y),
  (upper_right_x, upper_right_y)
]
"""
REGIONS_TO_SPLIT: List[List[Tuple[float, float]]] = [
    [
        (0, 420),
        (575, 750)
    ],
    [
        (0, 0),
        (575, 330)
    ],
]


def main() -> int:
    """
    Main function to initialise PDF Splitting.
    """

    clear_screen()
    welcome_screen()
    if (check_pre_reqs() == False):
        exit(1)

    skip_confirmation = has_arg('-s')
    show_progress = has_arg('-p')

    file_to_split = get_file_to_split(INPUT_DIR, skip_confirmation)
    if (file_to_split == False):
        exit(1)

    if (clear_directory(TEMP_DIR, skip_confirmation, show_progress) == False):
        exit(1)

    split_response = split_pdf(file_to_split, REGIONS_TO_SPLIT, TEMP_DIR, show_progress)
    if (split_response != 0):
        print(split_response)
        exit(1)

    ghost_export_response = ghost_export(
        TEMP_DIR, OUTPUT_DIR, skip_confirmation, show_progress)
    if (ghost_export_response):
        print(ghost_export_response)
        exit(1)

    if (clear_directory(TEMP_DIR, True, show_progress) == False):
        exit(1)

    print("\nSplitting Complete.")
    exit(0)


if (__name__ == '__main__'):
    main()

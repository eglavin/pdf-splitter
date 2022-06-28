#!/usr/bin/python
#
# References:
# https://pypdf2.readthedocs.io
# https://github.com/mstamy2/PyPDF2

from os import path
from glob import glob
from typing import Any, List, Tuple
from utilities import check_pdf_encryption, clear_output_directory, clear_screen, create_dir_if_not_exists, get_file_name_from_path, welcome_screen, confirm_choice
from PyPDF2 import PdfFileWriter, PdfFileReader

# Global Variables
#
INPUT_DIR = './input'
OUTPUT_DIR = './output'
REGIONS_TO_SPLIT = [
    [(0, 420), (575, 750)],
    [(0, 0), (575, 330)],
]


def save_page(page: Any, output_file_name: str) -> None:
    """
    Function to save PDF out to the given file name.
    """

    output_writer = PdfFileWriter()
    output_writer.addPage(page)

    print(f"Saving File: {output_file_name}")
    try:
        with open(output_file_name, "wb") as out_file:
            output_writer.write(out_file)
    except:
        exit(1)


def extract_region(page: Any, output_file_name: str, region: List[Tuple]) -> None:
    """
    Function to extract a region from a page.
    """

    try:
        page.trimBox.lowerLeft = region[0]
        page.trimBox.upperRight = region[1]

        page.cropBox.lowerLeft = region[0]
        page.cropBox.upperRight = region[1]
    except:
        print(f"Error Extracting Region from: {output_file_name}")
        exit(1)

    save_page(page, output_file_name)


def split_pdf(input_file_name: str) -> str | int:
    """
    Function to open the given PDF file and then split into individual pages.
    """

    with open(input_file_name, "rb") as input_file:
        pdf = PdfFileReader(input_file)

        if (check_pdf_encryption(pdf, input_file_name)):
            return "Encrypted PDF File, Unable To Open."

        count_pdf_pages = pdf.getNumPages()
        if (count_pdf_pages == 0):
            return "PDF File Has No Pages."

        if (create_dir_if_not_exists(f'{OUTPUT_DIR}/') == False):
            return "Error Creating Output Directory."

        print(
            f'\n{count_pdf_pages} pages to be split into {len(REGIONS_TO_SPLIT)} regions.')
        try:
            file_name = get_file_name_from_path(input_file_name)
            region_count = 0

            for page_number in range(count_pdf_pages):
                page = pdf.getPage(page_number)

                for region in REGIONS_TO_SPLIT:
                    region_count += 1

                    extract_region(
                        page,
                        f'{OUTPUT_DIR}/{file_name} - {region_count}.pdf',
                        region)

        except:
            return "An Error Occurred While Splitting Files."

    return 0


def get_file_to_split() -> str | bool:
    """
    Function to get latest file in the input directory.
    """

    try:
        # Get all files in the input directory.
        list_of_pdf_files = glob(f'{INPUT_DIR}/*.pdf')

        # Get the latest PDF file.
        latest_file = max(list_of_pdf_files, key=path.getmtime)

        # Confirm with user if they want to split the found file.
        print('Is this the file you want to split: ')
        print(f'\t{latest_file}')

        if (confirm_choice()):
            return latest_file
    except:
        print("No File Found.")

    return False


def main() -> int:
    """
    Main function to initialise PDF Splitting.
    """

    clear_screen()
    welcome_screen()

    file_to_split = get_file_to_split()
    if (file_to_split == False):
        exit(1)

    if (clear_output_directory(OUTPUT_DIR) == False):
        exit(1)

    output = split_pdf(file_to_split)
    if (output != 0):
        print(output)
        exit(1)

    print("\nSplitting Complete.")
    exit(0)


if (__name__ == '__main__'):
    main()

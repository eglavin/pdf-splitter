#!/usr/bin/python
#

from glob import glob
from sys import argv
from os import mkdir, path, remove, system, name
from pathlib import Path
from shutil import which
from typing import List, Tuple
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader, PageObject


def clear_screen() -> None:
    """
    Clear the screen for the next input.
    """

    if (name == 'nt'):
        _ = system('cls')
    else:
        _ = system('clear')


def welcome_screen() -> None:
    """
    Log welcome screen message.
    """

    print("Welcome to Payslipper - eglavin.com")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def check_pre_reqs() -> None | bool:
    """
    Function to check if the pre-requisites are met.
    """

    has_ghostscript: str
    if (name == 'nt'):
        has_ghostscript = which('gswin64c')
    else:
        has_ghostscript = which('gs')

    if (not has_ghostscript):
        print("Ghostscript not found. Please install Ghostscript.")
        return False


def has_arg(arg: str) -> bool:
    """
    Function to check if the given argument is present.
    """

    return arg in argv


def confirm_choice() -> bool:
    """
    Function to confirm the user wants to continue.
    """

    user_input = input("\nPress (c) to Continue or (e) to Exit: ").lower()

    if (user_input != 'c' and user_input != 'e'):
        print("Invalid Option. Please Enter A Valid Option.")
        return confirm_choice()

    if (user_input == 'e'):
        return False
    return True


def create_directory(dir: str) -> bool:
    """
    Create directory if it doesn't exist.
    """

    try:
        if (not path.exists(dir)):
            mkdir(dir)
            return True
    except:
        return False


def get_file_name_from_path(input_path: str) -> str:
    """
    Get the file name from the input file path.
    """

    return Path(input_path).stem


def clear_directory(dir: str, skip_confirmation: bool, show_progress: bool, file_type: str = 'pdf') -> bool | None:
    """
    Function to clear a directory contents of the given type of files.
    """

    files = glob(f'{dir}/*.{file_type}')
    if (len(files) > 0):
        print(
            f"\n{len(files)} files found in {dir} directory, deleting now.") if skip_confirmation else print(f"\n{len(files)} files found in {dir} directory would you like to delete them?")

        if (skip_confirmation or confirm_choice()):
            try:
                for file in files:
                    if show_progress:
                        print(
                            f'Removing: {dir}/{get_file_name_from_path(file)}.{file_type}')
                    remove(file)
            except:
                print("Error Clearing Directory.")
                return False
        else:
            return False


def get_file_to_split(input_directory: str, skip_confirmation: bool) -> str | bool:
    """
    Function to get latest pdf file in the given directory.
    """

    try:
        # Get all files in the input directory.
        list_of_pdf_files = glob(f'{input_directory}/*.pdf')

        # Get the latest PDF file.
        latest_file = max(list_of_pdf_files, key=path.getmtime)

        # Confirm with user if they want to split the found file.
        print('Found file: ') if skip_confirmation else print(
            'Is this the file you want to split: ')
        print(f'\t{input_directory}/{get_file_name_from_path(latest_file)}')

        if (skip_confirmation or confirm_choice()):
            return latest_file
    except:
        print("No File Found.")

    return False


def check_pdf_encryption(pdf: PdfReader) -> bool:
    """
    Check if the PDF file is encrypted.
    """

    if (pdf.is_encrypted):
        try:
            if (pdf.decrypt('') == 0):
                raise Exception('Error Decrypting PDF File.')
        except:
            return True

    return False


def save_page(page: PageObject, output_file_name: str, show_progress: bool) -> None:
    """
    Function to save PDF to the given file name.
    """

    output_writer = PdfWriter()
    output_writer.add_page(page)

    if show_progress:
        print(f"Saving: {output_file_name}")
    try:
        with open(output_file_name, "wb") as out_file:
            output_writer.write(out_file)
    except:
        exit(1)


def extract_region(page: PageObject, output_file_name: str, region: List[Tuple[float, float]], show_progress: bool) -> None:
    """
    Function to extract a region from a page.
    """

    try:
        page.trimbox.lower_left = region[0]
        page.trimbox.upper_right = region[1]

        page.cropbox.lower_left = region[0]
        page.cropbox.upper_right = region[1]
    except:
        print(f"Error Extracting Region from: {output_file_name}")
        exit(1)

    save_page(page, output_file_name, show_progress)


def split_pdf(input_file_name: str, regions_to_split: List[List[Tuple[float, float]]], output_directory: str, show_progress: bool) -> str | int:
    """
    Function to open the given PDF file and then split into individual pages.
    """

    with open(input_file_name, "rb") as input_file:
        pdf = PdfReader(input_file)

        if (check_pdf_encryption(pdf)):
            return "Encrypted PDF File, Unable To Open."

        count_pdf_pages = len(pdf.pages)
        if (count_pdf_pages == 0):
            return "PDF File Has No Pages."

        if (create_directory(f'{output_directory}/') == False):
            return "Error Creating Output Directory."

        print(
            f'\nFound {count_pdf_pages} pages to be split into {len(regions_to_split)} regions.')
        try:
            file_name = get_file_name_from_path(input_file_name)
            region_count = 0

            for page_number in range(count_pdf_pages):
                page = pdf.pages[page_number]

                for region in regions_to_split:
                    region_count += 1

                    extract_region(
                        page,
                        f'{output_directory}/{file_name} - {region_count}.pdf',
                        region,
                        show_progress)

        except:
            return "An Error Occurred While Splitting Files."

    return 0


def ghost_export(temp_directory: str, output_directory: str, skip_confirmation: bool, show_progress: bool) -> None | str:
    """
    Function to re-export the PDF files in the given temp directory to a 
    given output directory.
    """

    if (create_directory(f'{output_directory}/') == False):
        return "Error Creating Output Directory."

    if (clear_directory(output_directory, skip_confirmation, show_progress) == False):
        return "Error Clearing Output Directory."

    files = glob(f'{temp_directory}/*.pdf')
    if (len(files) == 0):
        return "No PDF Files Found In {temp_directory} Directory."

    print(f"\nExporting {len(files)} files with Ghostscript.")

    try:
        for file in files:
            if show_progress:
                print(
                    f"Exporting: {output_directory}/{get_file_name_from_path(file)}.pdf")
            if (name == 'nt'):
                system(f'gswin64c \
                    {"" if show_progress else "-q"} \
                    -dSAFER \
                    -dNOPAUSE \
                    -dBATCH \
                    -sDEVICE=pdfwrite \
                    -sOutputFile="{output_directory}/{get_file_name_from_path(file)}.pdf" \
                    "{file}"')
            else:
                system(f'gs \
                    {"" if show_progress else "-q"} \
                    -dSAFER \
                    -dNOPAUSE \
                    -dBATCH \
                    -sDEVICE=pdfwrite \
                    -sOutputFile="{output_directory}/{get_file_name_from_path(file)}.pdf" \
                    "{file}"')
    except:
        return "An Error Occurred While Exporting Files."

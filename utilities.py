#!/usr/bin/python
#

from glob import glob
from os import mkdir, path, remove, system, name
from pathlib import Path
from PyPDF2 import PdfReader
from datetime import datetime


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
    Logs the welcome screen.
    """

    print("Welcome to Payslipper - eglavin.com")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def confirm_choice() -> bool:
    """
    Function to confirm the user wants to continue.
    """

    user_input = input("\nPress (c) to Continue or (e) to Exit: ").lower()

    if (user_input != 'c' and user_input != 'e'):
        print("Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()

    if (user_input == 'e'):
        return False
    return True


def create_dir_if_not_exists(output_dir: str) -> bool:
    """
    Create the output directory if it doesn't exist.
    """

    try:
        if (not path.exists(output_dir)):
            mkdir(output_dir)
            return True
    except:
        return False


def clear_output_directory(output_directory) -> bool | None:
    """
    Function to clear the output directory.
    """

    if (len(glob(f'{output_directory}/*.pdf')) > 0):
        print("Files found in output directory would you like to delete them?")

        if (confirm_choice()):
            try:
                for file in glob(f'{output_directory}/*.pdf'):
                    print(f'Removing: {file}')
                    remove(file)
            except:
                print("Error Clearing Output Directory.")
                return False
        else : 
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


def get_file_name_from_path(input_file_name: str) -> str:
    """
    Get the file name from the input file path.
    """

    return Path(input_file_name).stem

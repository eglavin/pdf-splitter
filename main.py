#!/usr/bin/python
#
# Script to open PDF file,
# Read PDF file,
# Find Employees based on given array of employee names,
# Septate Each Employee into their own file.
#
# https://pythonhosted.org/PyPDF2/PageObject.html
# https://github.com/mstamy2/PyPDF2
# https://stackoverflow.com/questions/457207/cropping-pages-of-a-pdf-file
# https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
# https://www.manejandodatos.es/2014/11/ocr-python-easy/
# https://yasoob.me/2016/02/25/ocr-on-pdf-files-using-python/
# https://hub.docker.com/r/clearlinux/tesseract-ocr

from system import clearScreen, welcome
from PyPDF2 import PdfFileWriter, PdfFileReader
import glob
import os

clearScreen()
welcome()

# Outputs single PDF page

def printFile(ouput_page, file_name):
    output_data = PdfFileWriter()
    output_data.addPage(ouput_page)

    # output_data.addMetadata({'/Registered to': "test"})

    with open(file_name, "wb") as out_f:
        output_data.write(out_f)

    return


# Function used to split wage slips into their own files

def splitPages(input_file_name):
    with open(input_file_name, "rb") as input_file:
        pdf = PdfFileReader(input_file)

        if pdf.isEncrypted:
            try:
                pdf.decrypt('')
            except:
                print("Error Decrypting File.")
                exit()

        numOfPDFPages = pdf.getNumPages()

        # Print PDF Info
        print(f'{numOfPDFPages} pages to be split.')

        output_dir = './Split-Files/'
        output_prefix = "Wage Slip - "
        output_number = 0

        # Create Output dir if not already created
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Loop through pages and Split Wage slips into separate files
        try:
            for i in range(numOfPDFPages):
                # Cut Top Section of page
                output_number += 1
                top_page = pdf.getPage(i)
                top_page.trimBox.lowerLeft = (0, 420)
                top_page.trimBox.upperRight = (575, 750)
                top_page.cropBox.lowerLeft = (0, 420)
                top_page.cropBox.upperRight = (575, 750)

                output_file_name = f'{output_dir}{output_prefix} {output_number}.pdf'
                printFile(top_page, output_file_name)

                # Cut Bottom Section of page
                output_number += 1
                bottom_page = pdf.getPage(i)
                bottom_page.trimBox.lowerLeft = (0, 0)
                bottom_page.trimBox.upperRight = (575, 330)
                bottom_page.cropBox.lowerLeft = (0, 0)
                bottom_page.cropBox.upperRight = (575, 330)

                output2_file_name = f'{output_dir}{output_prefix} {output_number}.pdf'
                printFile(bottom_page, output2_file_name)
        except:
            return print("An error Occurred while splitting files.")
            exit()

    return print("Wage Splitting Completed.")


def confirmChoice():

    confirm_input = input("[c]Confirm or [e]Exit: ")

    if confirm_input != 'c' and confirm_input != 'e':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirmChoice()

    if confirm_input == 'e':
        exit()

    return confirm_input

# Main Function to read file data and export new file to root directory.

def main():

    # Gets the newest pdf file to be split.
    list_of_pdf_files = glob.glob('./*.pdf')
    latest_file = max(list_of_pdf_files, key=os.path.getctime)
    print(f'File to be Split: {latest_file}')

    confirmChoice()

    splitPages(latest_file)


main()

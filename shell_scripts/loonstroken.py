#!/home/cees/.virtualenvs/ceasaro_py/bin/python
# ####/usr/bin/python
import sys

from PyPDF2 import PdfWriter, PdfReader

OUTPUT_DIR = "/home/cees/Dropbox/Slagerij/Personeel"

def main(prog_args):
    if len(prog_args) != 2:
        exit("No pdf file specified! please run './loonstroken.py YOUR_PDF.pdf")
    pdf_file = prog_args[1]
    pdf = PdfReader(open(pdf_file, "rb"))

    for i in range(len(pdf.pages)):
        output = PdfWriter()
        pdf_page = pdf.pages[i]
        employee_name = None
        employee_nr = None
        for line in pdf_page.extract_text().splitlines():
            if "9742 AL Groningen" in line:
                employee_name = line.split(' ')[-1]
            if "Medewerker " in line:
                employee_nr = line.split("Medewerker ")[1]
                break

        output.add_page(pdf_page)
        new_filename = f"{OUTPUT_DIR}/loonstrook-{employee_nr}-{employee_name}.pdf"
        with open(new_filename, "wb") as outputStream:
            output.write(outputStream)
        print(f"Saved {new_filename}")

if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
from pdf_text_extract import text_extract_from_pdf
from search_criteria import file_name, company_text, ship_date_year
from directory_paths import rootdir, destination_dir
import os
import shutil


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        PDF_file = os.path.join(subdir, file)

        pdf_text = text_extract_from_pdf(PDF_file)

        year = ship_date_year(pdf_text)
        new_pdfname = file_name(pdf_text)
        company_name = company_text(pdf_text)

        print(company_name)
        print(year)
        print(new_pdfname)
        print('====================')

        # print(pdf_text)

        year_folders = os.listdir(destination_dir)

        if year in year_folders:
            year_subdirectory = destination_dir + f'\\{year}'
        else:
            try:
                year_subdirectory = destination_dir + f'\\{year}'
                os.mkdir(year_subdirectory)

            except FileExistsError as exc:
                print(exc)

        company_folders = os.listdir(year_subdirectory)

        if company_name in company_folders:
            company_subdirectory = year_subdirectory + f'\\{company_name}'
        else:
            try:
                company_subdirectory = year_subdirectory + f'\\{company_name}'
                os.mkdir(company_subdirectory)

            except FileExistsError as exc:
                print(exc)

        shutil.move(rootdir + fr'\{file}', company_subdirectory + fr'\{new_pdfname}.pdf')
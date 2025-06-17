"""
    The Website didn't allowed long connection when downloading pdf's
    So created this file which, does is from a csv file having the links 
    download the files one by one reading the csv. 
"""

import os
import csv
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning from urllib3 needed for ignoring SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a folder to save downloaded PDFs
if not os.path.exists("downloaded_pdfs"):
    os.makedirs("downloaded_pdfs")

# Read the CSV file
csv_file_path = "downloaded_pdfs_info.csv"
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    total_rows = sum(1 for row in csv_reader)  # Count the total number of rows
    csv_file.seek(0)
    # Skip the header row
    next(csv_reader, None)

    # for row in csv_reader:
    for index, row in enumerate(csv_reader, 1):
        pdf_name, text_from_td, download_link = row

        if not os.path.exists(f"downloaded_pdfs/{pdf_name}.pdf"): # check if a pdf is not already downloaded
            # Download the PDF
            print(f"({index}/{total_rows}) Downloading {pdf_name} from {download_link}")
            pdf_response = requests.get(download_link, verify=False)
            with open(f"downloaded_pdfs/{pdf_name}.pdf", 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            print(f"Downloaded {pdf_name}")

# Close the CSV file
csv_file.close()

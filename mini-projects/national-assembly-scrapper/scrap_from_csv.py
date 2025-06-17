import os
import time
import csv
from urllib.parse import urljoin

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Function to get select options data
def get_selectoptions_data(soup, id):
    """
        From select element , get it's options text and value
    :param soup:
    :param id:
    :return:
    """
    select_soup = soup.find(attrs={'id': id})
    values = []
    texts = []
    for option in select_soup.find_all('option'):
        values.append(option['value'].strip())
        texts.append(option.text.strip())
    return values, texts

# Create a folder to save downloaded PDFs
if not os.path.exists("downloaded_pdfs"):
    os.makedirs("downloaded_pdfs")

# Create and open a CSV file for writing
csv_file_path = "downloaded_pdfs_info.csv"
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    """
        This loop troll the tenure, year and the session select, 
        options one by one, with three loops and then finally gives
        back the csv filr and also can download the pdfs,
        as the code.
    """
    csv_writer = csv.writer(csv_file)
    # Write header to the CSV file
    csv_writer.writerow(["PDF Name", "Text from 2nd last <td>", "Download Link"])

    URL = "https://na.gov.pk/en/debates.php"
    driver = webdriver.Chrome()
    driver.get(URL)

    # Wait for the page to fully load (adjust the time as needed)
    driver.implicitly_wait(10)

    # Initialize BeautifulSoup with WebDriver's page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the submit button
    submit_button = driver.find_element(By.CLASS_NAME, "mybtn")

    # Get the select options data for tenure
    tenure_select = Select(driver.find_element(By.ID, 'tenure_id'))
    year_select = Select(driver.find_element(By.ID, 'py_id'))
    session_select = Select(driver.find_element(By.ID, 'select_session'))

    tenure_values = [option.get_attribute('value') for option in tenure_select.options]

    # Iterate through each combination of tenure, year, and session
    for tenure_value in tenure_values:
        # Select the values in the tenure dropdown
        if tenure_value != '':
            tenure_select.select_by_value(tenure_value)
            # Wait for a brief moment for the next dropdown to update (adjust the time as needed)
            time.sleep(2)
            # Get the select options data for year
            year_values = [option.get_attribute('value') for option in year_select.options]
            for year_value in year_values:
                if year_value != '':
                    year_select.select_by_value(year_value)

                    time.sleep(3)

                    # Get the select options data for session
                    session_values = [option.get_attribute('value') for option in session_select.options]
                    for session_value in session_values:
                        if session_value != '':
                            session_select.select_by_value(session_value)

                            # Click the submit button
                            submit_button.click()
                            print("clicked")

                            # Wait for the page to load after clicking submit (adjust the time as needed)
                            time.sleep(2)

                            # Get the updated page source
                            soup = BeautifulSoup(driver.page_source, 'html.parser')

                            # Find the table
                            table = driver.find_element(By.CLASS_NAME, 'mytable1')
                            rows = table.find_elements(By.TAG_NAME, 'tr')

                            # Iterate through each row in the table
                            for row in rows[1:]:  # Skip the header row
                                columns = row.find_elements(By.TAG_NAME, 'td')
                                if len(columns) >= 3:
                                    # Extract text from the second last <td>
                                    pdf_name = columns[-2].text.strip()
                                    print(f"Pdf is {pdf_name}")

                                    # Extract the PDF URL
                                    link = row.find_elements(By.TAG_NAME, 'a')
                                    if link:
                                        pdf_relative_path = link[0].get_attribute('href')
                                        pdf_absolute_path = urljoin("https://na.gov.pk/", pdf_relative_path.replace("../", ""))

                                        # Write information to the CSV file
                                        csv_writer.writerow([pdf_name, columns[-2].text.strip(), pdf_absolute_path])

                                        # Download the PDF
                                        print(f"Downloading {pdf_name}")
                                        pdf_response = requests.get(pdf_absolute_path)
                                        with open(f"downloaded_pdfs/{pdf_name}.pdf", 'wb') as pdf_file:
                                            pdf_file.write(pdf_response.content)
                                        print(f"Downloaded {pdf_name}")

# Close the CSV file
csv_file.close()

# Close the browser
driver.quit()

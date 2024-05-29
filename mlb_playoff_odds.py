import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from io import StringIO
from typing import List, IO

# Set up Selenium
service: Service = Service()
options: webdriver.ChromeOptions = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
options.add_argument('--no-sandbox')  # Bypass OS security model, needed for running in Docker
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
driver: webdriver.Chrome = webdriver.Chrome(service=service, options=options)

# URL to scrape
url: str = "https://www.fangraphs.com/standings/playoff-odds"

# Navigate to the page
driver.get(url)

# Wait for the tables to load
wait: WebDriverWait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'playoff-odds-table')))

# Get the page source and parse with BeautifulSoup
soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all tables with class "playoff-odds-table"
tables: List[BeautifulSoup] = soup.find_all('table', class_='playoff-odds-table')

# Print the number of tables found
print(f"Number of tables found: {len(tables)}")

# with open('output_tables.txt', 'w', encoding='utf-8') as file:
#     # Iterate through each table and write its HTML content to the text file
#     for index, table in enumerate(tables):
#         html_content: str = str(table)  # Convert BeautifulSoup object to HTML string
#         file.write(f"Table {index + 1}:\n")
#         file.write(html_content)
#         file.write("\n\n")  # Add a separator between tables

# Print the HTML content of each table
for index, table in enumerate(tables):
    html_str: str = str(table)
    html_io: IO[str] = StringIO(html_str)
    df_list: List[pd.DataFrame] = pd.read_html(html_io)
    for df_index, df in enumerate(df_list):
        output_filename: str = f'output_table_{index + 1}_{df_index + 1}.csv'
        df.to_csv(output_filename, index=False)

# Close the Selenium driver
driver.quit()

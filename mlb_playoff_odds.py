from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import List

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

# Print the HTML content of each table
for index, table in enumerate(tables):
    print(f"\nTable {index + 1}:")
    print(table.prettify())

# Close the Selenium driver
driver.quit()

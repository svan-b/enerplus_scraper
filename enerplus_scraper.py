import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Directory for PDFs
base_dir = r"C:\Users\vanbo\OneDrive\Documents\Onedrive\Desktop\Python\Enerplus scrape\downloads"
os.makedirs(base_dir, exist_ok=True)

# ChromeDriver path
chrome_driver_path = r'C:\Selenium\chromedriver.exe'

# Headless mode options
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Target URL
url = 'https://investors.enerplus.com/reports-filings/quarterly-results/default.aspx'
driver.get(url)

# Wait for elements to load
driver.implicitly_wait(10)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.doc.doc-link"))
)

# Parsing HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())  # Optional: Remove after confirming the correct page loads

# Finding links
links = soup.find_all('a', class_='doc doc-link')
print(f"Found {len(links)} 'doc doc-link' links. Attempting to download PDFs:")

for link in links:
    href = link.get('href')
    if href and href.endswith('.pdf'):
        full_url = f"https://investors.enerplus.com{href}" if href.startswith('/') else href
        filename = os.path.join(base_dir, os.path.basename(href))
        
        print(f"Downloading: {full_url}")
        response = requests.get(full_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {full_url}")

driver.quit()
print("Selenium WebDriver has been shut down in headless mode.")

import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Define the directory where PDFs will be saved
base_dir = r"C:\Users\vanbo\OneDrive\Documents\Onedrive\Desktop\Python\Enerplus scrape\downloads"
os.makedirs(base_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Set the path to your chromedriver executable
chrome_driver_path = r'C:\Selenium\chromedriver.exe'  # Update this path

# Set options for headless mode
options = Options()
options.headless = True  # No browser GUI

# Create a Service object and pass it to the driver with options
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Define the URL of the page you want to scrape
url = 'https://investors.enerplus.com/reports-filings/quarterly-results/default.aspx'

# Use Selenium to get the page
driver.get(url)

# Get the HTML content after JavaScript has loaded
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find all hyperlinks with the class 'doc doc-link'
links = soup.find_all('a', class_='doc doc-link')

# Print the total number of links found and details for each link
print(f"Found {len(links)} 'doc doc-link' links. Attempting to download PDFs:")

for link in links:
    href = link.get('href')
    if href.endswith('.pdf'):
        # Construct the full URL if needed
        full_url = f"https://investors.enerplus.com{href}" if href.startswith('/') else href
        filename = os.path.join(base_dir, os.path.basename(href))  # Set the filename and directory
        
        # Download and save the PDF
        print(f"Downloading: {full_url}")
        response = requests.get(full_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {full_url}")

# Close the Selenium WebDriver
driver.quit()
print("Selenium WebDriver has been shut down in headless mode.")

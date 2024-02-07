from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Set the path to your chromedriver executable
service = Service('C:\\Selenium\\chromedriver.exe')
driver = webdriver.Chrome(service=service)


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
print(f"Found {len(links)} 'doc doc-link' links. Printing details:")

for link in links:
    href = link.get('href')
    text = link.get_text(strip=True)
    print(f"Link text: {text}, Href: {href}")

# Close the Selenium WebDriver
driver.quit()

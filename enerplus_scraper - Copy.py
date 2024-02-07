import requests
from bs4 import BeautifulSoup

# Define your headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Define the URL of the page you want to scrape
url = 'https://investors.enerplus.com/reports-filings/quarterly-results/default.aspx'

# Send an HTTP request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully accessed the page!")
    
    # Parse the content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print out the entire HTML content
    print(soup.prettify())  # This will print the entire HTML

    # Find all hyperlinks with the class 'doc doc-link'
    links = soup.find_all('a', class_='doc doc-link')
    
    # Print the total number of links found and details for each link
    print(f"Found {len(links)} 'doc doc-link' links. Printing details:")
    
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        # Construct the full URL if needed
        full_url = f"https://investors.enerplus.com{href}" if href.startswith('/') else href
        print(f"Link text: {text}, Full URL: {full_url}")

else:
    print("Failed to access the page, status code:", response.status_code)

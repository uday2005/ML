from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import pprint

# --- Configuration ---
LOGIN_URL = "http://quotes.toscrape.com/login"
# For this example, we scrape the main page after login.
SCRAPE_URL = "http://quotes.toscrape.com/"
CSV_FILE = "quotes.csv"
# In a real project, NEVER hardcode credentials. Use environment variables.
USERNAME = "admin"
PASSWORD = "admin"

print("--- Starting Scraper ---")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # --- 1. LOGIN PROCESS ---
    print(f"Navigating to login page: {LOGIN_URL}")
    page.goto(LOGIN_URL)

    # Use robust locators to find form fields and fill them
    print("Filling in login credentials...")
    page.get_by_label("Username").fill(USERNAME)
    page.get_by_label("Password").fill(PASSWORD)
    
    # Find the login button by its role and click it
    page.get_by_role("button", name="Login").click()

      # Wait for the page to navigate away from /login, confirming success
    print("Waiting for login to complete...")
    page.wait_for_url("**/", timeout=10000) # Wait for URL to NOT be /login
    print("✅ Login Successful!")

     # --- 2. SCRAPING PROCESS ---
    print(f"Navigating to scrape target: {SCRAPE_URL}")
    page.goto(SCRAPE_URL)

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    scraped_data = []
    quote_containers = soup.find_all('div', class_='quote')

    for container in quote_containers:
        # --- 3. DATA EXTRACTION & CLEANING ---
        text = container.find('span', class_='text').get_text(strip=True)
        author = container.find('small', class_='author').get_text(strip=True)
        
        cleaned_text = text.strip('“”')

        tags_list = [tag.get_text(strip=True) for tag in container.find_all('a', class_='tag')]
        tag_string = "|".join(tags_list)

        scraped_data.append({
            'quote': cleaned_text,
            'author': author,
            'tags': tag_string
        })

    browser.close()
    print(f"✅ Scraping complete. Found {len(scraped_data)} quotes.")

print(f"Saving data to {CSV_FILE}...")
# Define the headers for our CSV file
fieldnames = ['quote', 'author', 'tags']

try:
    # 'w' is for write mode. 'newline=""' prevents blank rows. 'encoding' handles all characters.
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        # Create a DictWriter object
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write all our scraped data
        writer.writerows(scraped_data)
        
    print(f"✅ Data successfully saved to {CSV_FILE}.")

except IOError as e:
    print(f"❌ Error saving file: {e}")

# Let's print one record to see our clean data
print("\nSample of cleaned data:")
pprint.pprint(scraped_data[0])
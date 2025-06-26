import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv
import pprint

# --- PART 1: CONFIGURATION ---
# All values that might change are grouped here for easy access.
class Config:
    START_URL = "http://books.toscrape.com/index.html"
    BASE_URL = "http://books.toscrape.com/" # For resolving relative URLs
    CSV_FILE = "structured_books.csv"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

# --- PART 2: THE SCRAPER CLASS ---
# The class encapsulates all scraping logic. It has a clear responsibility.
class BookScraper:
    def __init__(self, start_url, base_url, headers):
        """Initializes the scraper with necessary URLs and headers."""
        self.current_url = start_url
        self.base_url = base_url
        self.headers = headers
        self.scraped_data = []
        self.page_count = 1

    def _get_page_content(self):
        """Handles the request and returns a BeautifulSoup object or None."""
        print(f"Scraping page {self.page_count}: {self.current_url}")
        try:
            response = requests.get(self.current_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"URL request failed: {self.current_url}. Error: {e}")
            return None

    def _parse_page(self, soup):
        """Parses a single page and extracts all book data."""
        books_on_page = []
        book_containers = soup.find_all('article', class_='product_pod')
        for book in book_containers:
            title = book.find('h3').find('a')['title']
            price = book.find('p', class_='price_color').get_text(strip=True)
            rating_text = book.find('p', class_='star-rating')['class'][1]
            
            # Simple data cleaning
            cleaned_price = (price.replace('£', ''))
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            cleaned_rating = rating_map.get(rating_text, 0)
            
            books_on_page.append({
                'title': title,
                'price': cleaned_price,
                'rating': cleaned_rating
            })
        return books_on_page

    def _get_next_page_url(self, soup):
        """Finds the 'Next' button and returns the full URL for the next page."""
        next_button = soup.find('li', class_='next')
        if next_button:
            relative_url = next_button.find('a')['href']
            # We need to resolve this relative to the base URL of the *catalogue*
            return urljoin(self.current_url, relative_url)
        return None

    def run_scraper(self):
        """The main orchestration method for the scraper."""
        while self.current_url:
            soup = self._get_page_content()
            if not soup:
                break # Stop if a page request fails
            
            page_data = self._parse_page(soup)
            self.scraped_data.extend(page_data)
            
            self.current_url = self._get_next_page_url(soup)
            self.page_count += 1
            time.sleep(1) # Be respectful
        
        print("\n✅ Scraping complete.")

# --- PART 3: DATA STORAGE ---
# This function is now separate and reusable. Its only job is to save data.
def save_to_csv(data, filename, fieldnames):
    """Saves a list of dictionaries to a CSV file."""
    print(f"Saving {len(data)} records to {filename}...")
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print("✅ Data successfully saved.")
    except IOError as e:
        print(f"❌ Error saving file: {e}")

# --- PART 4: THE EXECUTION BLOCK ---
# This block only runs when the script is executed directly.
if __name__ == "__main__":
    # 1. Create an instance of our scraper with the configuration.
    scraper = BookScraper(
        start_url=Config.START_URL,
        base_url=Config.BASE_URL,
        headers=Config.HEADERS
    )
    
    # 2. Run the scraper. It will populate its own 'scraped_data' attribute.
    scraper.run_scraper()
    
    # 3. Save the results.
    if scraper.scraped_data:
        save_to_csv(
            data=scraper.scraped_data,
            filename=Config.CSV_FILE,
            fieldnames=['title', 'price', 'rating']
        )
        print("\n--- Process Complete ---")
        print("Sample of scraped data:")
        pprint.pprint(scraper.scraped_data[:3])
    else:
        print("No data was scraped.")
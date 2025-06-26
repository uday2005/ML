import requests
from bs4 import BeautifulSoup
# Removed lxml import since it's causing issues
import pprint
import time
from urllib.parse import urljoin



BASE_URL = "http://books.toscrape.com/catalogue/" 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

all_books_data = []

page_num = 1
URL_to_scrape = "http://books.toscrape.com/index.html"

REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def make_request(url):
    attempt = 0
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url,headers=HEADERS,timeout=REQUEST_TIMEOUT)

            response.raise_for_status()
            # it will raise HTTPS exception  if the server sent back the error code.
            # if it is succesful it will do nothing.
            return response
        
        # if it will give timeout then this will come as error 
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt + 1}: Timeout while requesting {url}")


        except requests.exceptions.HTTPError as e:

            if e.response.status_code in [500,502,503,504]:
                print(f"Attempt {attempt + 1}: Server Error ({e.response.status_code}) for {url}. Retrying...")
            else:
                # For other errors (like 404 Not Found), retrying won't help.
                print(f"Attempt {attempt + 1}: Client Error ({e.response.status_code}) for {url}. Aborting.")
                return None # Abort for this URL
        
        except requests.exceptions.RequestException as e:
            # Catch any other request-related errors (e.g., DNS issues)
            print(f"Attempt {attempt + 1}: A request error occurred: {e}")

        # If we are not on the last attempt, wait before retrying
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (2 ** attempt))

        attempt = attempt +1
    # If all retries fail
    print(f"All {MAX_RETRIES} attempts failed for URL: {url}")
    return None
        


while URL_to_scrape:
    print(f"Scraping page {page_num}: {URL_to_scrape}")
            
    try:
        response = make_request(URL_to_scrape)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Could not request URL {URL_to_scrape}. Error: {e}")
        # If one page fails, we can choose to continue or break. Let's continue.
        break

    soup = BeautifulSoup(response.text,'html.parser')
    print(response.url)

    book_containers = soup.find_all('article' ,class_='product_pod')

    if not book_containers:
        print(f"No books found on page {page_num}. Stopping.")
        break

    
    for book in book_containers:
        book_name = book.find('h3').find('a')['title']
        book_price = book.find('p',class_='price_color').get_text(strip=True) # This get test wil get text of that class 
        bookp_rating = book.find('p', class_= 'star-rating')
        book_rating = bookp_rating['class'][1] 
        # this will give class as a list to acess it as we are not using get text

        scraped_data = {
            'name' : book_name,
            'price' : book_price,
            'rating' : book_rating
        }
        all_books_data.append(scraped_data)

    next_button_li = soup.find('li', class_='next')

    if next_button_li:
        # If the button is found, get the relative URL from the <a> tag inside it
        relative_url = next_button_li.find('a')['href']
        # Use urljoin to safely combine the base URL and the relative path
        URL_to_scrape = urljoin(response.url, relative_url)
        # URL_to_scrape = urljoin(BASE_URL, relative_url)
        page_num += 1 # Increment our page counter
    else:
        # If no "Next" button is found, we are on the last page.
        print("No 'next' button found. Reached the last page.")
        URL_to_scrape = None # Set this to None to terminate the while loop

   # --- Be a Respectful Scraper: Pause between requests ---
    time.sleep(1) # Wait for 1 second before scraping the next page

print("\n--- SCRAPING COMPLETE ---")
print(f"Successfully scraped {len(all_books_data)} books across {page_num} pages.")
print("Here is a sample of the first 5 books:")
pprint.pprint(all_books_data[:5])


# so in the first page we haev index.html as last text on url so we assume that urljoin will join the url directly but
# it is smart and what happen is that when it encounted some text leike url index.html or anything so it go one previous 
# and then add that to that 
# response.url gives the url of that accessing webpage.

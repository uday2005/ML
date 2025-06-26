import requests
import pprint
import time

API_URL_TEMPLATE = "https://quotes.toscrape.com/api/quotes?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    # While not strictly required for this API, it's good practice to include these
    # for APIs discovered via XHR requests.
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

all_quotes_data = []

# --- The Scraping Loop ---
page_num = 1
while True:
    URL_scrapper = API_URL_TEMPLATE.format(page_num)

    try:
        response = requests.get(URL_scrapper,headers=HEADERS , timeout = 10)
        response.raise_for_status()
        
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        break

    quotes_on_page = data.get('quotes', [])

    for quote_dict in quotes_on_page:
        all_quotes_data.append({
            'text': quote_dict.get('text'),
            'author': quote_dict.get('author', {}).get('name'), # Safely access nested key
            'tags': quote_dict.get('tags')
        })

#     The key you want to access.
# (Optional) A default value to return if the key is not found.

#  You need the complex get(..., {}).get(...) pattern for nested objects. For simple, non-nested values, get(...) is fine, 
# and providing a default like [] or '' is a good practice for data consistency. Your instinct was spot on.

    if not data.get('has_next'):
        print("Reached the last page of the API.")
        break

    page_num += 1
    time.sleep(1)


print("\n--- SCRAPING COMPLETE ---")
print(f"Successfully scraped {len(all_quotes_data)} quotes from the API.")
print("Sample of the first 5 quotes:")
pprint.pprint(all_quotes_data[:5])
print("\nSample of the last 5 quotes:")
pprint.pprint(all_quotes_data[-5:])


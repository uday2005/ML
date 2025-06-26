
# Import the necessary functions and classes from our libraries.
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import time
import pprint


# Define constants at the top. This makes the script easier to read and modify.
URL = "http://quotes.toscrape.com/js/"

# --- 3. DATA STORAGE ---
# Initialize an empty list to hold all the data we scrape.
# We define it outside the main block so it's accessible at the end.
all_quotes_data = []
page_count = 1

print("--- Starting Playwright Scraper ---")

# --- 4. THE MAIN PLAYWRIGHT BLOCK ---
# 'sync_playwright()' starts the Playwright service.
# The 'with' statement is a context manager. It guarantees that even if
# our script crashes, the browser and service will be shut down cleanly.
with sync_playwright() as p:
    
    # --- 5. LAUNCHING THE BROWSER ---
    # 'p.chromium' tells Playwright to use the Chromium browser engine.
    # '.launch()' starts a new browser instance.
    # 'headless=True' means the browser runs invisibly in the background.
    # For debugging, set 'headless=False' to open a real browser window and watch.
    browser = p.chromium.launch(headless=False) 
    
    # Create a new "tab" or "page" in the browser.
    page = browser.new_page()
    
    # --- 6. INITIAL NAVIGATION ---
    # Command the browser page to navigate to our target URL.
    # 'timeout=60000' sets a 60-second limit for this navigation to complete.
    # This prevents the script from hanging forever on a slow-loading site.
    page.goto(URL, timeout=60000)
    print(f"✅ Navigated to: {URL}")

    # --- 7. THE PAGINATION LOOP ---
    # 'while True' creates an infinite loop. We will use the 'break' statement
    # inside the loop to exit it when we detect we're on the last page.
    while True:
        print(f"\n--- Scraping Page {page_count} ---")
        
        # --- 8. EXPLICIT WAIT (THE SAFETY NET) ---
        # This is a critical command. It tells Playwright: "PAUSE the script here
        # and do not proceed until you can find at least one element on the page
        # that matches the CSS selector 'div.quote'". This ensures the page's
        # JavaScript has finished loading the initial quotes before we try to scrape.
        page.wait_for_selector("div.quote")
        
        # --- 9. THE HYBRID TECHNIQUE: GETTING HTML FOR BEAUTIFULSOUP ---
        # 'page.content()' takes a snapshot of the page's current HTML, *after*
        # all the JavaScript has run and modified the DOM. This is the "live" source code.
        html_content = page.content()
        
        # We now pass this fully-rendered HTML to BeautifulSoup, because its API
        # for finding and extracting data is very convenient and powerful.
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # --- 10. SCRAPING THE CURRENT PAGE ---
        # This is now standard BeautifulSoup code, just like in Module 1.
        quote_containers = soup.find_all('div', class_='quote')
        print(f"Found {len(quote_containers)} quotes on this page.")
        
        for container in quote_containers:
            text = container.find('span', class_='text').get_text(strip=True)
            author = container.find('small', class_='author').get_text(strip=True)
            # Append the extracted data as a dictionary to our main list.
            all_quotes_data.append({'text': text, 'author': author})
        
        # --- 11. HANDLING PAGINATION (THE LOOP'S EXIT STRATEGY) ---
        # We wrap this logic in a 'try...except' block to handle the case
        # where the "Next" button might disappear completely from the HTML.
        try:
            # Create a Playwright 'Locator' object. This is a "recipe" for finding
            # the 'Next' button. We're looking for an <a> tag inside an <li> with class 'next'.
            next_button_locator = page.locator("li.next > a")
            
            # Use the locator to check if the button is disabled. On the last page,
            # the button becomes greyed out, which Playwright can detect.
            # We give it a 'timeout' of 5 seconds because the button's state might
            # take a moment to update after the page loads.
            if next_button_locator.is_disabled(timeout=5000):
                print("➡️ 'Next' button is disabled. Reached the last page.")
                break # This command exits the 'while True' loop.

            # If the button is not disabled, we click it. Playwright's auto-waiting
            # ensures it will wait for the button to be clickable before this action.
            print("➡️ Clicking 'Next' button...")
            next_button_locator.click()
            
            # Increment our page counter for logging purposes.
            page_count += 1
            
            # This is a simple but effective pause. After clicking 'Next', the page's
            # JavaScript is busy fetching new data and re-drawing the page. This pause
            # gives it a moment to settle before the 'while' loop restarts.
            time.sleep(1) 

        # This 'except' block will run if the 'is_disabled' command times out,
        # which means the locator "li.next > a" could not find any element at all.
        except TimeoutError:
            print("➡️ 'Next' button not found. Assuming last page.")
            break # Exit the 'while True' loop.
            
    # --- 12. CLEANUP ---
    # This code runs after the 'while' loop has been exited by a 'break' statement.
    print("\n✅ All pages scraped. Closing browser.")
    # It's crucial to close the browser to free up system resources.
    browser.close()

# --- 13. FINAL OUTPUT ---
# This code runs after the 'with' block has completed.
print(f"\n--- SCRAPING COMPLETE ---")
print(f"Successfully scraped {len(all_quotes_data)} quotes from {page_count} pages.")
print("Sample of the first 5 quotes:")
# 'pprint' is "pretty-print", which formats dictionaries and lists nicely.
pprint.pprint(all_quotes_data[:5])
print("\nSample of the last 5 quotes:")
pprint.pprint(all_quotes_data[-5:])



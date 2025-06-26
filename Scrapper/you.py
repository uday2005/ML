from playwright.sync_api import sync_playwright, TimeoutError
import time
from bs4 import BeautifulSoup
import csv
import pprint


with sync_playwright() as p:
    current_url = 'https://www.iplt20.com/auction/2019'
    browser = p.chromium.launch(headless=False) # Can be True or False
    page = browser.new_page()
    print("Extracting final HTML content...")
        # We target the body tag to get everything visible.
    page.goto(current_url, wait_until="load", timeout=60000)
    body_html = page.locator("body").inner_html()
    


    with open('ipl_page_source2019.html', 'w', encoding='utf-8') as file:
        file.write(body_html)
    
    print("HTML saved to 'ipl_page_source.html'")
    browser.close()

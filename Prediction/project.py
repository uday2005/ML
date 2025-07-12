from playwright.sync_api import sync_playwright, TimeoutError
import time
from bs4 import BeautifulSoup
import csv
import pprint



def parse_htm_content (html_content,year):
    team_players = []
    soup = BeautifulSoup(html_content , 'html.parser')

    full_team_name = soup.find('h2')
    full_team_name_final = full_team_name.get_text(strip=True) if full_team_name else "Unknown Team"

    
    all_tables_body = soup.find_all('tbody', id='pointsdata') 
    if all_tables_body:
        all_tables_body = all_tables_body
    else:
        all_tables_body = soup.find_all('tbody')
    # find will be still fine i was thinking others thing that why one extra loop in
    # form of all tables body which runs only one time as tbody is only one time

    for i in range(len(all_tables_body)):
        team_name = full_team_name_final

        for tables in all_tables_body:
            data = tables.find_all('tr')
            for rows in data:
                table_data = rows.find_all('td')

                player_name = table_data[1].get_text(strip=True)
                # Nationality = table_data[2].get_text(strip=True)
                # Type = table_data[3].get_text(strip=True)
                if year==2025:
                    price = table_data[3].get_text(strip=True).replace("₹","")
                else:
                    price = table_data[-1].get_text(strip=True).replace("₹","")


                team_players.append(
                    {
                        "Year" : year,
                        "TeamName": team_name,
                        "PlayerName": player_name,
                        # "Nationality": Nationality,
                        # "Type": Type,
                        "Price": price,
                    }
                )
            
    return team_players



# --- Configuration ---
URL = 'https://www.iplt20.com/auction/{}'
OUTPUT_FILE = 'ipl_page_source.html'
# Let's give the page a generous amount of time to settle down after the initial load.
WAIT_AFTER_LOAD = 10 # seconds

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Can be True or False
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    all_players_data = []
    for i in range(2025,2017,-1):
        current_url = URL.format(i)
        print(f"Navigating to: {current_url}")
        # 'load' waits for the 'load' event to be fired. It's a good baseline.
        page.goto(current_url, wait_until="load", timeout=60000)
        print("Page has loaded.")

        # --- Handle Cookie Banner ---
        # It's important to do this first, as it can prevent other content from loading.
        try:
            accept_button = page.get_by_role("button", name="Accept Cookies")
            # Give it a few seconds to appear
            accept_button.wait_for(state="visible", timeout=7000)
            accept_button.click()
            print("✅ Cookie banner handled.")
        except TimeoutError:
            print("No cookie banner found. Proceeding.")
        
        # --- Wait for JavaScript to Settle ---
        # This is a simple but effective way to wait for client-side rendering to complete.
        print(f"Waiting for {WAIT_AFTER_LOAD} seconds for the page to stabilize...")
        time.sleep(WAIT_AFTER_LOAD)
        print("Wait complete.")

        # --- Get the Final HTML ---
        print("Extracting final HTML content...")
        # We target the body tag to get everything visible.
        body_html = page.locator("body").inner_html()

        print("Parsing the HTML string with BeautifulSoup...")
        # Create the BeautifulSoup object from the string
        soup = BeautifulSoup(body_html, 'html.parser')

        team_sections = soup.find_all('section', id=lambda x: x and x.endswith('-inside'))

        # --- STRATEGY 2: If the first strategy found nothing, try the "old" selector ---
        if not team_sections:
            print("Modern structure not found. Falling back to older structure (class='ih-points-table-sec')...")
            team_sections = soup.find_all('section', class_='ih-points-table-sec')

        print(f"Found {len(team_sections)} team sections for year {i} using the determined structure.")

        if not team_sections:
            print(f"Warning: No team data sections could be found for year {i} with any known method.")
            # 'continue' will skip to the next year in your main loop
            continue
        
        
        for section in team_sections:
            # Pass the HTML of each section to our parsing function
            # section.prettify() turns the BeautifulSoup tag object back into a string
            section_html = section.prettify()
            players = parse_htm_content(section_html,i)
            # Add the returned list of players to our main list
            all_players_data.extend(players)

    browser.close()


fieldnames = ["Year","TeamName" ,"PlayerName","Price"]
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

save_to_csv(all_players_data,'ipl.csv' ,fieldnames=fieldnames)
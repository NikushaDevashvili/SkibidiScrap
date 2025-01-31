import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # For better stability in headless mode

# Set up the Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)  # Update path to your chromedriver if necessary

# Open the main page with infinite scroll
driver.get("https://read.cv/explore/activity")

# Store all profile links in a set (to avoid duplicates)
all_profile_links = set()


# Open the file for writing the profile links
with open('profile_links.txt', 'w') as file:

    # Keep scrolling as long as the page keeps loading new profiles and the time limit hasn't been reached
    previous_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(4)  # Adjust the sleep time to give the page enough time to load

        # Get new height after scrolling
        current_height = driver.execute_script("return document.body.scrollHeight")
        
        # Parse the current page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all profile links on the current page and add them to the set
        new_links = {a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/')}
        
        # Update the set with new links and immediately write them to the file
        for link in new_links:
            all_profile_links.add(link)
            file.write(f"https://read.cv{link}\n")  # Write each link to the file as it is found

        # If the page height hasn't changed, stop scrolling
        if current_height == previous_height:
            break

        # Update the previous height
        previous_height = current_height

# Close the driver
driver.quit()

print("Profile links have been saved to profile_links.txt")
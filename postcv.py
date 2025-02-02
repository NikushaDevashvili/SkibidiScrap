import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # For better stability in headless mode

# Set up the Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the main page
driver.get("https://posts.cv/")

# Wait for the page to load
wait = WebDriverWait(driver, 100)

try:
    # Locate the "Everyone" tab using a more reliable XPath selector
    everyone_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Everyone')]")))
    everyone_tab.click()
    time.sleep(3)  # Wait for the content to update
except Exception as e:
    print("Could not find or click the 'Everyone' tab:", e)

# Store all usernames in a set (to avoid duplicates)
all_usernames = set()
count = 0  # Counter for real-time tracking

# Open the file for writing the profile links
with open('postcvusernames.txt', 'w', buffering=1) as file:  # buffering=1 enables line buffering (real-time saving)
    
    # Keep scrolling as long as the page keeps loading new profiles
    previous_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(4)  # Slower scrolling

        # Get new height after scrolling
        current_height = driver.execute_script("return document.body.scrollHeight")
        
        # Parse the current page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all <span class="Post_username__eI9DD"> elements
        username_spans = soup.find_all('span', class_="Post_username__eI9DD")

        # Extract usernames only from <a> tags inside these spans
        for span in username_spans:
            a_tag = span.find('a', href=True)
            if a_tag and a_tag['href'].startswith('/'):
                username = a_tag['href'].lstrip('/')  # Remove the leading '/'
                profile_link = f"https://read.cv/{username}"

                if profile_link not in all_usernames:
                    all_usernames.add(profile_link)
                    file.write(profile_link + "\n")  # Write each link to the file
                    file.flush()  # Ensure it's saved immediately
                    
                    count += 1  # Increase counter
                    print(f"Collected {count} usernames so far...")  # Print in terminal in real time

        # If the page height hasn't changed, stop scrolling
        if current_height == previous_height:
            break

        # Update the previous height
        previous_height = current_height

# Close the driver
driver.quit()

print(f"Scraping complete! Total usernames collected: {count}")
print("Usernames have been saved to postcvusernames.txt in the format https://read.cv/username")
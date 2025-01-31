import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # For better stability in headless mode

# Set up the Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)  # Update path to your chromedriver if necessary

# Open the main page with infinite scroll
driver.get("https://read.cv/explore/activity")

# Keep scrolling as long as the page keeps loading new profiles
previous_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll to the bottom
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)  # Adjust the sleep time to give the page enough time to load

    # Get new height after scrolling
    current_height = driver.execute_script("return document.body.scrollHeight")
    
    # If the page height hasn't changed, stop scrolling
    if current_height == previous_height:
        break
    
    # Update the previous height
    previous_height = current_height

# Now get the page source after scrolling
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all profile links (Adjust the tag and class based on the page structure)
profile_links = {a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/')}

# Save the unique profile links to a .txt file
with open('profile_links.txt', 'w') as file:
    for link in profile_links:
        file.write(f"https://read.cv{link}\n")

# Close the driver
driver.quit()

print("Profile links have been saved to profile_links.txt")
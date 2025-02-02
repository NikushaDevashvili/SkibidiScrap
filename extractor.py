from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Selenium WebDriver (assuming using Chrome)
driver = webdriver.Chrome()

# Open the website
driver.get("https://read.cv/explore")

# Allow page to load
time.sleep(3)

# Find and click the search button
search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
search_button.click()

# Allow the popup to load
time.sleep(2)

# Scroll down to trigger infinite scroll
def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down a bit
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for new profiles to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_load()

# Loop through search results
while True:
    # Find the first profile
    profile_links = driver.find_elements(By.XPATH, "//a[@class='profile-link']")  # Update the XPath if necessary
    if profile_links:
        profile_links[0].click()

        # Wait for profile to load
        time.sleep(3)

        # Try to extract the email
        try:
            email = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]").text
            print(f"Email: {email}")
        except:
            print("No email found.")

        # Go back to the search results
        driver.back()

        # Scroll again to the same position after going back
        scroll_to_load()
    else:
        print("No profiles left to scrape.")
        break

# Close the driver when done
driver.quit()
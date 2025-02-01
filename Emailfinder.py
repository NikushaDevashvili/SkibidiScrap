import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')

csv_file_path = 'hrefs-list.csv'

# Read links from the links.csv file
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    links = [row[0] for row in reader]  # Assuming links are in the first column

# Initialize the webdriver
driver = webdriver.Chrome(options=chrome_options)

# Function to extract emails from the page source
def extract_emails(page_source):
    # Use regex to find emails in the page source
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_source)
    return set(emails)  # Return a unique set of emails

# Open the email file for writing
with open('mails.txt', 'w') as email_file:
    for link in links:
        link = link.strip()
        if not link:
            continue
        
        print(f"Opening link: {link}")  # Debug print to show which link is being opened
        try:
            driver.get(link)  # Open the link
            time.sleep(3.5)  # Wait for the page to load
            page_source = driver.page_source  # Get the page source
            emails = extract_emails(page_source)  # Extract emails from page source
            
            if emails:
                print(f"Found emails: {emails}")  # Debug print to show emails found
                for email in emails:
                    email_file.write(email + '\n')  # Write each email to the file as it's found
                    email_file.flush()  # Ensure emails are flushed to disk immediately
            else:
                print(f"No emails found on {link}")  # Debug print if no emails found
            
        except Exception as e:
            print(f"Error opening {link}: {e}")

# Close the browser
driver.quit()

print(f"Emails saved to mails.txt.")
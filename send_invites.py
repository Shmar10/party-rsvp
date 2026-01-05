import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuration
CSV_FILE = 'guests.csv'
VERCEL_URL = '[YOUR_VERCEL_URL]'
BASE_URL = 'https://messages.google.com/web'

def send_invites():
    # Load guests
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return
    
    df = pd.read_csv(CSV_FILE)
    
    # Initialize Selenium Client
    print("Launching Chrome...")
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    
    print("\n" + "="*50)
    print("ACTION REQUIRED: Scan the QR code on your phone to link Google Messages.")
    input("Once you are logged in and see your conversations, press Enter here to continue...")
    print("="*50 + "\n")
    
    wait = WebDriverWait(driver, 30)
    
    for index, row in df.iterrows():
        name = row['Name']
        phone = str(row['Phone'])
        
        print(f"[{index+1}/{len(df)}] Sending invite to {name} ({phone})...")
        
        try:
            # 1. Click 'Start chat'
            # Using a more robust XPath for the Start chat button
            start_chat_xpath = "//div[contains(text(), 'Start chat') or contains(text(), 'Start Chat')]"
            start_chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, start_chat_xpath)))
            start_chat_btn.click()
            
            # 2. Enter phone number
            # The input for phone number usually appears in a specific field
            phone_input_xpath = "//input[@placeholder='Type a name, phone number, or email']"
            phone_input = wait.until(EC.presence_of_element_located((By.XPATH, phone_input_xpath)))
            phone_input.send_keys(phone)
            time.sleep(1) # Small buffer for the dropdown to appear
            phone_input.send_keys(Keys.ENTER)
            
            # 3. Wait for the message input to load
            msg_input_xpath = "//textarea[@placeholder='Text message']"
            msg_input = wait.until(EC.presence_of_element_located((By.XPATH, msg_input_xpath)))
            
            # 4. Type and send message
            message = f"Hey {name}! Hope you can make it. RSVP here: {VERCEL_URL}"
            msg_input.send_keys(message)
            time.sleep(1)
            msg_input.send_keys(Keys.CONTROL + Keys.ENTER)
            
            print(f"Successfully sent to {name}.")
            
            # 5. Cool down to avoid spam detection
            print("Waiting 10 seconds before next message...")
            time.sleep(10)
            
        except Exception as e:
            print(f"Failed to send to {name}: {str(e)}")
            # Optional: try to navigate back to base URL if stuck
            driver.get(BASE_URL)
            time.sleep(5)

    print("\nAll invites processed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    send_invites()

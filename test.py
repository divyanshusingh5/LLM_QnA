from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def setup_driver():
    # Create Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Example option

    # Set up ChromeDriver with options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    return driver

def handle_popup(driver):
    try:
        # Switch to the iframe where the popup might be present
        driver.switch_to.frame("iFrmLinks")
        
        # Wait for the "Stay signed out" button to be clickable and click it
        stay_signed_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Stay signed out"]'))
        )
        stay_signed_out_button.click()
        print("Clicked on 'Stay signed out' button")
        
        # Switch back to the default content after handling the popup
        driver.switch_to.default_content()
        
    except Exception as e:
        print(f"No popup appeared or error occurred: {e}")

def upload_image_and_search(driver, image_path):
    # Navigate to Google Images
    driver.get("https://www.google.com/imghp")

    # Handle potential "Stay signed out" popup
    handle_popup(driver)
    
    # Click the camera icon to start image search
    camera_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.Q4LuWd"))
    )
    camera_icon.click()

    # Wait for the "Upload an image" tab to be visible and click it
    upload_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="Upload an image"]'))
    )
    upload_tab.click()

    # Locate the file input element and upload the image
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    file_input.send_keys(image_path)

    # Wait for results to load
    time.sleep(5)  # Adjust if necessary

    # Extract image URLs
    image_urls = set()
    while len(image_urls) < 10:  # Ensure we fetch only up to 10 images
        thumbnails = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i"))
        )
        for thumbnail in thumbnails:
            if len(image_urls) >= 10:
                break
            try:
                thumbnail.click()
                time.sleep(1)  # Adjust if necessary
                full_image = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.n3VNCb"))
                )
                src = full_image.get_attribute('src')
                if src and 'http' in src:
                    image_urls.add(src)
            except Exception as e:
                print(f"Error occurred while extracting image URL: {e}")

        # Scroll down to load more images if needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust if necessary
    
    return image_urls

def main():
    driver = setup_driver()
    try:
        # Path to the image you want to upload
        image_path = r'D:\Prompt-Design\myimage.png'
        
        # Ensure the image path is correct
        if not os.path.isfile(image_path):
            print("The specified image path does not exist.")
            return
        
        # Perform image upload and search
        image_urls = upload_image_and_search(driver, image_path)
        
        # Print fetched image URLs (up to 10)
        for url in image_urls:
            print(url)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

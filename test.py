import sys
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def google_reverse_search(target, image_base64):
    google_images_url = "https://images.google.com/"

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if needed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup ChromeDriver
    service = Service(executable_path="/path/to/chromedriver")  # Update the path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(google_images_url)
        
        # Click on the "Search by image" button
        camera_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sbtc"]/div/div[2]/div[2]/a'))
        )
        camera_icon.click()
        
        # Click on "Upload an image" tab
        upload_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="qbug"]/div/a'))
        )
        upload_tab.click()
        
        # Upload the image
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="qbug"]/div/div[2]/input'))
        )
        image_path = "/path/to/image.png"  # Path to a local image file if base64 is not used
        with open(image_path, "wb") as file:
            file.write(base64.b64decode(image_base64))
        upload_input.send_keys(image_path)
        
        # Wait for the results to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'rso'))
        )
        
        # Check if the target is present in the search results
        results = driver.page_source
        if target in results:
            print(f"{target} found in search results.")
            return True
        else:
            print(f"{target} not found in search results.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        target = sys.argv[1]
        image_base64 = sys.argv[2]
        google_reverse_search(target, image_base64)
    else:
        print("Usage: python script.py <target> <base64_image>")

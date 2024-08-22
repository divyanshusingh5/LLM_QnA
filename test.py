from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import ImageGrab  # To capture the screenshot
import pyautogui
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def capture_screenshot(image_path):
    # Capture a screenshot of the entire screen
    screenshot = ImageGrab.grab()  # Use PIL to capture the screenshot
    screenshot.save(image_path)

def paste_image(driver, image_path):
    try:
        # Navigate to Google Lens
        driver.get('https://lens.google.com')

        # Capture the screenshot
        capture_screenshot(image_path)

        # Find the upload area using XPath or another selector
        upload_area = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )

        # Click the upload area to focus it (make sure it's visible and clickable)
        upload_area.click()

        # Wait a bit to ensure the area is ready to receive input
        time.sleep(2)

        # Simulate pasting the screenshot using pyautogui
        pyautogui.hotkey('ctrl', 'v')

        # Wait for the results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "results-container")]'))
        )

        # Extract similar image links
        links = []
        similar_images = driver.find_elements(By.XPATH, '//a[contains(@href, "imgres")]')
        for img in similar_images[:10]:
            link = img.get_attribute('href')
            if link:
                links.append(link)

        return links

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

def main():
    driver = setup_driver()
    try:
        image_path = 'screenshot.png'  # Path where the screenshot will be saved
        similar_image_links = paste_image(driver, image_path)
        if similar_image_links:
            print("Top 10 similar image links:")
            for link in similar_image_links:
                print(link)
        else:
            print("No similar images found or an error occurred.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from Screenshot import Screenshot  # Ensure you have the Screenshot library installed

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def capture_screenshot(driver, image_path):
    ob = Screenshot.Screenshot()
    img_url = ob.full_screenshot(driver, save_path=image_path, image_name='screenshot.png', is_load_at_runtime=True, load_wait_time=3)
    return img_url

def paste_image(driver, image_path):
    try:
        # Navigate to Google Lens or similar service
        driver.get('https://lens.google.com')

        # Wait for the upload area to be clickable
        upload_area = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )

        # Capture the screenshot
        capture_screenshot(driver, image_path)

        # Simulate pasting the screenshot into the upload area
        # Since pasting is complex and not directly supported, you might need to rely on the file upload approach.

        # Use ActionChains to move to the upload area and then paste (if supported)
        actions = ActionChains(driver)
        actions.move_to_element(upload_area).click().perform()

        # Set the file path into the file input element
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(image_path + 'screenshot.png')

        # Wait for the results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "results-container")]'))
        )

        # Extract similar image links
        links = []
        similar_images = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "imgres")]'))
        )
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
        image_path = 'D:/Prompt-Design/'  # Path where the screenshot will be saved
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

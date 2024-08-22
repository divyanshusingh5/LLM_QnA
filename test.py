from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def handle_sign_in_popup(driver):
    try:
        # Switch to the iframe that contains the pop-up (if necessary)
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@name="signin_frame"]'))  # Replace with actual iframe name or ID if required
        )

        # Click "Stay signed out" or dismiss the popup
        stay_signed_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="stay_signed_out_button_xpath"]'))  # Replace with actual button XPath
        )
        stay_signed_out_button.click()

        # Switch back to the main content after handling the popup
        driver.switch_to.default_content()
        print("Handled sign-in pop-up.")
        
    except Exception as e:
        print(f"Failed to handle the sign-in popup: {e}")

def upload_image_and_find_similar(driver, image_path):
    try:
        # Navigate to Google Lens or a similar service
        driver.get('https://lens.google.com')

        # Handle the sign-in popup if it appears
        handle_sign_in_popup(driver)

        # Use the provided full XPath to upload the image
        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/c-wiz/div[2]/div/div[3]/div[2]/div/div[2]/span'))
        )
        upload_button.click()

        # Upload the image file
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(image_path)

        # Wait for the results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "results-container")]'))
        )

        # Extract the top 10 similar image links
        links = []
        similar_images = driver.find_elements(By.XPATH, '//a[contains(@href, "imgres")]')  # Adjust this if needed
        for img in similar_images[:10]:
            links.append(img.get_attribute('href'))

        return links

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

def main():
    driver = setup_driver()
    try:
        image_path = 'D:/Prompt-Design/myimage.png'  # Replace with the actual path to your image
        similar_image_links = upload_image_and_find_similar(driver, image_path)
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

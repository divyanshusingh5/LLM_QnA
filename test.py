from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def handle_sign_in_popup(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@name="signin_frame"]'))
        )
        stay_signed_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="stay_signed_out_button_xpath"]'))
        )
        stay_signed_out_button.click()
        driver.switch_to.default_content()
        print("Handled sign-in pop-up.")
        
    except Exception as e:
        print(f"Failed to handle the sign-in popup: {e}")

def upload_image_and_find_similar(driver, image_path):
    try:
        driver.get('https://lens.google.com')

        handle_sign_in_popup(driver)

        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/c-wiz/div[2]/div/div[3]/div[2]/div/div[2]/span'))
        )
        upload_button.click()

        time.sleep(2)

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        
        # Debugging: Verify the file input element
        print("File input found. Uploading image...")
        print(f"File input element details: {file_input.get_attribute('outerHTML')}")

        # Upload the image
        file_input.send_keys(image_path)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "results-container")]'))
        )

        links = []
        similar_images = driver.find_elements(By.XPATH, '//a[contains(@href, "imgres")]')
        for img in similar_images[:10]:
            links.append(img.get_attribute('href'))

        return links

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

def main():
    driver = setup_driver()
    try:
        image_path = 'D:\\Prompt-Design\\myimage.png'  # Use double backslashes or forward slashes
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

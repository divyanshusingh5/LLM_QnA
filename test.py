from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# Set up the ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

try:
    # Navigate to Google Images
    driver.get('https://images.google.com')
    driver.maximize_window()

    # Handle the "Stay signed out" prompt if it appears
    try:
        # Wait for the iframe if present
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
        )
        # Wait for the "Stay signed out" button to be clickable and click it
        stay_signed_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/c-wiz/div/div/c-wiz/div/div/div/div[2]/div[2]/button'))
        )
        stay_signed_out_button.click()
        print("Clicked 'Stay signed out' button.")
    except Exception as e:
        print(f"No 'Stay signed out' button found or error occurred: {e}")

    # Click on the "Search by image" button (typically represented as a camera icon)
    search_by_image_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-attrid="image"]'))
    )
    search_by_image_button.click()

    # Click on the "Upload an image" tab
    upload_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[text()="Upload an image"]'))
    )
    upload_tab.click()

    # Click the "Choose file" button and upload the image
    choose_file_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    image_path = os.path.abspath('D:\\Prompt-Design\\myimage.png')  # Ensure the path is correct
    choose_file_button.send_keys(image_path)

    # Wait for the response and extract the top 5 links
    response_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rg_meta'))
    )
    
    # Extracting the image result links
    links = []
    response_elements = response_element.find_elements(By.CSS_SELECTOR, 'a')
    for link in response_elements[:5]:
        link_url = link.get_attribute('href')
        if link_url:
            links.append(link_url)

    print(links)

finally:
    # Close the browser
    driver.quit()

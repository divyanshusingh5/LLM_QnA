from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

try:
    # Navigate to Google Lens
    driver.get('https://lens.google.com')
    driver.maximize_window()

    # Handle the "Stay signed out" prompt if it appears
    try:
        # Switch to the iframe if the button is inside one
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
        )
        # Wait for the "Stay signed out" button to be clickable and then click it
        stay_signed_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/c-wiz/div/div/c-wiz/div/div/div/div[2]/div[2]/button'))
        )
        stay_signed_out_button.click()
        print("Clicked 'Stay signed out' button.")
    except Exception as e:
        print(f"No 'Stay signed out' button found or error occurred: {e}")

    # Find the search button using XPath
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="lensSearchButton"]'))
    )

    # Click the search button
    search_button.click()

    # Upload an image
    # Replace 'path/to/image.jpg' with the actual path to your image
    image_path = 'D:\Prompt-Design\myimage.png'
    image_element = driver.find_element(By.NAME, 'file')
    image_element.send_keys(image_path)

    # Click the upload button (assuming it has an XPath like '//*[@id="uploadButton"]')
    upload_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="uploadButton"]'))
    )
    upload_button.click()

    # Wait for the response
    # You can use WebDriverWait to wait for the response to load
    response_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="response"]'))
    )

    # Extract the top 5 links
    links = []
    response_elements = response_element.find_elements(By.XPATH, './/a')
    for link in response_elements[:5]:
        link_url = link.get_attribute('href')
        links.append(link_url)

    print(links)

finally:
    # Close the browser
    driver.quit()

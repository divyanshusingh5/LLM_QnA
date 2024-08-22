from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get('https://www.google.com.br')
    driver.maximize_window()

    # Wait for potential iFrame and switch to it if needed
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name='callout']")))

    # Wait for the "Not Now" button to be clickable and click it
    not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Agora não']"))
    )
    not_now_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

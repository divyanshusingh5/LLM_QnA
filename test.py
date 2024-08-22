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
    driver.get('https://www.example.com')  # Replace with your website URL
    driver.maximize_window()

    # Close or bypass the login prompt
    try:
        # Wait for the login prompt to be present and then close it
        login_prompt_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']"))  # Update selector as needed
        )
        login_prompt_close_button.click()
        print("Login prompt closed.")
    except Exception as e:
        print(f"No login prompt found or error occurred: {e}")

    # Optionally, handle the "Log Out" option if needed
    try:
        # Wait for the "Log Out" button to be clickable and then click it
        log_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Log Out']"))  # Update selector as needed
        )
        log_out_button.click()
        print("Logged out successfully.")
    except Exception as e:
        print(f"No log out button found or error occurred: {e}")

    # Continue with other interactions on the website

finally:
    driver.quit()

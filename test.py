from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up ChromeDriver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to Google Images
driver.get("https://images.google.com")

# Handle the sign-in popup if it appears
try:
    stay_signed_out_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='signIn'] button"))
    )
    stay_signed_out_button.click()
except Exception as e:
    print("Sign-in popup did not appear or could not handle it:", e)

# Click on the 'Search by image' button using the provided selector
search_by_image_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#lensSearchButton"))
)
search_by_image_button.click()

# Wait for the shadow DOM to load
time.sleep(3)

# Access shadow DOM to find the file input element
shadow_root = driver.execute_script(
    "return document.querySelector('body > ntp-app').shadowRoot.querySelector('#realbox').shadowRoot"
)
file_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="file"]')

# Path to the image you want to upload
image_path = 'D:/Prompt-Design/myimage.png'

# Upload the image
file_input.send_keys(image_path)

# Wait for the image to be processed and results to be displayed
time.sleep(10)  # Adjust as needed based on image processing time

# Scroll to load more images if necessary
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find image elements
images = driver.find_elements(By.CSS_SELECTOR, "a.W4P4ne")
count = 1
links = []

for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element(By.XPATH, '//img[contains(@class, "n3VNCb")]').get_attribute("src")
        links.append(imgUrl)
        if len(links) >= 5:
            break
    except Exception as e:
        print("Error retrieving image URL:", e)
        continue

# Print the top 5 image URLs
for i, link in enumerate(links):
    print(f"Image {i + 1}: {link}")

# Close the browser
driver.quit()

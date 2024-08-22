from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    # Create Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Example option
    
    # Set up ChromeDriver with options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    return driver

def handle_popup(driver):
    try:
        # Wait for the "Stay signed out" button to be clickable and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Stay signed out"]'))
        ).click()
        print("Clicked on 'Stay signed out' button")
    except Exception as e:
        print(f"No popup appeared or error occurred: {e}")

def search_images(driver, query, max_links_to_fetch):
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver.get(search_url)
    
    # Handle potential "Stay signed out" popup
    handle_popup(driver)
    
    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0

    while image_count < max_links_to_fetch and error_clicks < 30:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep time if needed
        
        # Get all image thumbnail results
        thumbnail_results = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links...")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            try:
                img.click()
                time.sleep(1)  # Adjust sleep time if needed
            except Exception:
                error_clicks += 1
                print(f"ERROR: Unable to Click the Image ({error_clicks} errors)")
                continue
            
            # Extract image URLs
            actual_images = driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                src = actual_image.get_attribute('src')
                if src and 'http' in src:
                    image_urls.add(src)
            
            image_count = len(image_urls)
            print(f"Current Total Image Count: {image_count}")
            if image_count >= max_links_to_fetch:
                print(f"Found: {image_count} image links, done!")
                break
            
            # Click the "Load more" button if available
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
                if load_more_button:
                    driver.execute_script("arguments[0].click();", load_more_button)
            except Exception:
                print("No 'Load more' button found or error occurred")
                break
        
        results_start = len(thumbnail_results)
    
    return image_urls

def main():
    driver = setup_driver()
    try:
        # Perform image search
        query = "Manchester City"  # Example query
        max_links_to_fetch = 10    # Number of image URLs to fetch
        image_urls = search_images(driver, query, max_links_to_fetch)
        
        # Print fetched image URLs
        for url in image_urls:
            print(url)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

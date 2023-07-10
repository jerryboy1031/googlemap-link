from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set the path to the WebDriver executable
webdriver_path = 'path/to/chromedriver'

# Set any desired options for the WebDriver
options = Options()
options.add_argument("--headless")  # Run the browser in headless mode (without opening a window)

# Set up the WebDriver service
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    url = 'https://www.example.com'  # Replace with the actual URL of the tourist spot webpage
    driver.get(url)

    # Locate the price level element
    xpath = "//span[@class='price-level']"
    price_level_element = driver.find_element(By.XPATH, xpath)

    # Extract the price level
    price_level = price_level_element.text

    # Print or process the price level
    print("Price level:", price_level)

finally:
    # Clean up
    driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# `extract_website(string)` in 'auto-search-onsheets-machine' repo
# search by google search engine(Chrome) and extract the search result 
def extract_website2(search_query):
    # Configure Selenium
    driver_path = "/chromedriver_win32/chromedriver.exe" # Path to your ChromeDriver executable
    options = Options()
    options.headless = True  # Run the browser in headless mode (without GUI)
    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    # extend the pages (or the search results will only the first page)
    search_results = []
    # only scrape results from the first page (change as needed)
    url = f"https://www.google.com/search?q={search_query}&start=10"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Find search result elements
    search_results.extend(soup.find_all("div", class_="yuRUbf"))
    time.sleep(5) # wait 
    # Extract data from search results
    result= search_results[0]
    title = result.find("h3").get_text()
    url = result.find("a")["href"]
    print(title,url)
    # extract the content of the website
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #HTML tags
    print("title: ",title)
    if soup.find("h1") != None:
        print("h1: ",soup.find("h1").get_text())
    if soup.find("h2") != None:
        print("h2: ",soup.find("h2").get_text())
    if soup.find("h3") != None:
        print("h3: ",soup.find("h3").get_text())
    if soup.find("h4") != None:    
        print("h4: ",soup.find("h4").get_text())
    #print("h5: ",soup.find("h5").get_text())
    #print("h6: ",soup.find("h6").get_text())
    #print("body: ",soup.find("body").get_text())
    if soup.find("p") != None:
        print("p: ",soup.find("p").get_text())
    #print("ul: ",soup.find("ul").get_text())
    if soup.find("table") != None:
        print("table: ",soup.find("table").get_text())

    '''content_arr = soup.find_all("h3")
    
    for content in content_arr:
        if content.get_text() != "":
            each.append(content.get_text())
        else: 
            break
             
        
        
    #save data to sheets
    saveToSheet(results_data)'''

    # Close the browser
    driver.quit()
 
    
extract_website2('台中麗寶樂園門票價格')
'''# Set the path to the WebDriver executable
webdriver_path = "/chromedriver_win32/chromedriver"

# Set any desired options for the WebDriver
options = Options()
#options.add_argument("--headless")  # Run the browser in headless mode (without opening a window)

# Set up the WebDriver service
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    url = 'https://www.example.com'  # Replace with the actual URL of the tourist spot webpage
    driver.get(url)

    # Locate the price level element
    xpath = "//span[@class='price-level']"
    price_level_element = driver.find_element(By.XPATH, xpath) # error

    # Extract the price level
    price_level = price_level_element.text

    # Print or process the price level
    print("Price level:", price_level)

finally:
    # Clean up
    driver.quit()'''

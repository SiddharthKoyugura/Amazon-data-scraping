from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set the path to the ChromeDriver executable
chrome_driver_path = "D:\Apps\chromedriver.exe"

# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set up the ChromeDriver service
service = Service(chrome_driver_path)

# Create a new instance of the Chrome driver
def get_seller_names(url):
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open a webpage
    driver.get(url)

    prices = driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
    prices = prices[::2]
    sellers = []
    for price in prices:
        price.click()
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])

        status = driver.find_element(By.XPATH, '//*[@id="availability"]/span')

        if status.text == "In stock":
            seller = driver.find_element(By.XPATH, '//*[@id="merchant-info"]/a[1]/span')
            sellers.append(seller.text)
        else:
            sellers.append("Out of Stock")

        # Close the current tab
        driver.close()
        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])
    return sellers
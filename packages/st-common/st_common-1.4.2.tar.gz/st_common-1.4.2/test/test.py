from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_chrome_driver(debuggerAddress: str):
    # Create an instance of ChromeOptions
    chrome_options = Options()
    
    # Set the debugger address
    chrome_options.debugger_address = debuggerAddress
    
    # Example of adding other Chrome options or experimental options
    chrome_prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "download.default_directory": "D:\\Downloads"
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    
    # Add more options if needed
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

if __name__ == "__main__":
    # Example usage
    debugger_address = '127.0.0.1:9222'
    driver = create_chrome_driver(debuggerAddress=debugger_address)
    
    # Perform actions using the driver
    driver.get("http://www.google.com")
    print(driver.title)
    driver.quit()
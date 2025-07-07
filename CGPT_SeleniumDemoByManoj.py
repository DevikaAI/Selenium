from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)  # ✅ Initialize the explicit wait

# Open the website
driver.get("https://the-internet.herokuapp.com/")

# Navigate actions
driver.back()
driver.forward()
driver.refresh()

# ✅ Wait for the content div to be present
try:
    element = wait.until(EC.presence_of_element_located((By.ID, "content")))
    print("✅ Element found:", element.text)
except:
    print("❌ Element with ID 'content' not found.")

# ✅ Locate the first link using XPath
try:
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/ul/li[1]/a')))
    print("✅ First link found:", element.text)
except:
    print("❌ Could not locate the first link.")

# ✅ Click on the link
element.click()

# ✅ Take a screenshot
driver.save_screenshot("demo.png")
print("✅ Screenshot saved as demo.png")

# ✅ Close browser after short wait
import time
time.sleep(2)
driver.quit()

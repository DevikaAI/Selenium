from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Chrome options to block password popups and avoid automation detection
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# ✅ Start driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Login to remove password popup
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success")))
    print("✅ Logged in successfully.")

    # Step 2: Go to JS alert page
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    time.sleep(1)  # ensure render

    # Step 3: Try clicking alert button
    try:
        alert_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
        alert_btn.click()
    except:
        # 🔁 JS fallback click
        print("⚠️ Fallback: Using JavaScript to click.")
        driver.execute_script("document.querySelector('button[onclick=\"jsAlert()\"').click()")

    # Step 4: Handle alert
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("✅ Alert Text:", alert.text)
    alert.accept()

    # Step 5: Get result text
    result = driver.find_element(By.ID, "result").text
    print("✅ Alert result:", result)

except Exception as e:
    print("❌ Error occurred:", str(e))
    driver.save_screenshot("error_screenshot.png")
    print("📸 Screenshot saved: error_screenshot.png")

finally:
    time.sleep(1)
    driver.quit()

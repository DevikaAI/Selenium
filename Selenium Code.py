from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Configure Chrome options to fully suppress password manager
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.notifications": 2,
})

# ✅ Initialize Chrome
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # 1️⃣ Login Page (Triggers password manager, now blocked)
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    success_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success")))
    print("✅ Login Successful:", success_msg.text.strip())

    # 2️⃣ JavaScript Alert test
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    time.sleep(1)  # Ensure full render

    alert_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
    alert_button.click()

    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("✅ JS Alert Text:", alert.text)
    alert.accept()

    result = driver.find_element(By.ID, "result").text
    print("✅ Alert Result:", result)

except Exception as e:
    print("❌ Error occurred:", str(e))
    driver.save_screenshot("error_screenshot.png")
    print("📸 Screenshot saved: error_screenshot.png")

finally:
    time.sleep(2)
    driver.quit()

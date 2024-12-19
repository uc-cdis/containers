from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


opts = FirefoxOptions()
opts.add_argument('--headless')
browser = webdriver.Firefox(options=opts)

print("Checking for .lic file")
with open("/usr/local/stata18/stata.lic", "r", encoding="utf-8") as lic_file:
    print("Found stata.lic file")

print("Ready to open notebook")
browser.get("http://127.0.0.1:8888/lw-workspace/proxy/notebooks/licensed_stata_session.ipynb")
print("Notebook is opened")

actions = ActionChains(browser)
actions.pause(5)
actions.perform()
browser.save_screenshot('0.png')
# Down-arrow to get to the second cell in the notebook
actions.send_keys(Keys.DOWN)
actions.pause(1)
actions.perform()
browser.save_screenshot('1.png')
#actions.perform()
#browser.save_screenshot('1-1.png')
# Run the stata setup cell
print("Ready to run stata setup cell")
actions.key_down(Keys.SHIFT)
actions.send_keys(Keys.ENTER)
actions.key_up(Keys.SHIFT)
actions.pause(5)
actions.perform()
browser.save_screenshot('2.png')

#print("Ready to run stata setup cell2")
#actions.key_down(Keys.SHIFT)
#actions.send_keys(Keys.ENTER)
#actions.key_up(Keys.SHIFT)
#actions.pause(10)
#actions.perform()
#browser.save_screenshot('2-1.png')

# Save notebook with output
print("Ready to save notebook")
actions.key_down(Keys.CONTROL)
actions.send_keys("S")
actions.key_up(Keys.CONTROL)
actions.pause(5)
actions.perform()
actions.send_keys(Keys.ENTER)
actions.pause(1)
actions.perform()
browser.save_screenshot('3.png')

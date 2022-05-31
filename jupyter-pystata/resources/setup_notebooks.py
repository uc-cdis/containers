from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


print("Configuring headless webdriver...")
opts = Options()
# opts.headless = True
browser = webdriver.Firefox(options=opts)


print("Loading jupyterlab...")
browser.get("http://127.0.0.1:8888/lab")
time.sleep(10)


with open("/usr/local/stata17/stata.lic", "r") as lic_file:

    print("Stata license", lic_file.read())

for i, nb_launcher in enumerate(
    filter(
        lambda el: "Stata" in el.text,
        browser.find_elements(By.CLASS_NAME, "jp-DirListing-item")
    )
):
    print(f"Initializing Stata session {i+1}")
    actions = ActionChains(browser)

    # open notebook
    actions.double_click(nb_launcher)
    actions.pause(1)

    # run first cell
    actions.key_down(Keys.SHIFT)
    actions.send_keys(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.pause(1)

    # save notebook with output
    actions.key_down(Keys.CONTROL)
    actions.send_keys("S")
    actions.key_up(Keys.CONTROL)
    actions.pause(1)
    actions.send_keys(Keys.ENTER)

    actions.perform()

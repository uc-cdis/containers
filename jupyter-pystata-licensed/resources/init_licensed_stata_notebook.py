from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time


FIRST_CELL_SELECTOR="div.cell:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) >div:nth-child(1) > div:nth-child(1) > textarea:nth-child(1)"

opts = Options()
opts.headless = True
browser = webdriver.Firefox(options=opts)
browser.get("http://127.0.0.1:8888/lw-workspace/proxy/notebooks/licensed_stata_session.ipynb")
time.sleep(1)

form = browser.find_element_by_css_selector(FIRST_CELL_SELECTOR)
form.send_keys(Keys.CONTROL + Keys.ENTER)
time.sleep(1)

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

def get_screen_shot(url):
        service = Service(executable_path='C:/Users/aravind.palepu/Downloads/edgedriver_win64/msedgedriver.exe')
        options = Options()
        # options.add_argument("--headless=new") 
        options.add_argument("--disable-gpu")
        driver = webdriver.Edge(service=service, options=options)
        driver.get(url)
        time.sleep(3)
        screenshot_path = r"C:\Users\aravind.palepu\Python - Scripts\jetSetAccess\jetSetAccess\assets\screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

get_screen_shot("https://github.com/microsoft/NLWeb") 
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def html_obj(first, second=None):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        url = f'{first}{second}' if second is not None else f'{first}'
        driver.get(url=url)
        html = driver.page_source

        return html

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.webdriver.listener import WebDriverListener
from src.utils.webdriver.extended import WebDriverExtended
from selenium.webdriver.chrome.service import Service as ChromeService


class DriverFactory:
    @staticmethod
    def get_driver(config) -> WebDriverExtended:
        browser = config["browser"]
        if browser == "chrome":

            options = webdriver.ChromeOptions()

            options.page_load_strategy = "eager"

            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            if config["headless_mode"] is True:
                options.add_argument("--headless")
            driver_path = ChromeDriverManager().install()
            driver = WebDriverExtended(
                webdriver.Chrome(service=ChromeService(driver_path), options=options),
                WebDriverListener(), config
            )

            return driver
        raise Exception("Provide valid driver name")

import allure


class Base:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Opening page")
    def open(self):
        self.driver.open()

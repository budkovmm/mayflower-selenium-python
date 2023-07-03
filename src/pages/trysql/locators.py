from selenium.webdriver.common.by import By


class TrySqlLocator:
    run_sql_button = (By.XPATH, "//button[contains(text(),'Run SQL')]")
    result_table = (By.XPATH, "//*[@id=\"divResultSQL\"]//table")
    result_text = (By.XPATH, "//*[@id=\"divResultSQL\"]//div")

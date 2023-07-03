import logging

import pandas as pd

from src.pages.trysql.locators import TrySqlLocator
from src.pages.base import Base
import allure


class TrySQL(Base):
    logger = logging.getLogger()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Running SQL")
    def run_sql(self):
        self.driver.find_element(*TrySqlLocator.run_sql_button).click()

    @allure.step("Getting result table")
    def get_result_table(self):
        return self.driver.find_element(*TrySqlLocator.result_table)

    @allure.step("Getting result text")
    def get_result_text(self):
        return self.driver.find_element(*TrySqlLocator.result_text).text

    @allure.step("Filling query form")
    def fill_query_form(self, request: str):
        self.logger.info(f"SQL: {request}")
        script = f'window.editor.setValue("{request}")'
        self.driver.execute_script(script)

    @allure.step("Getting dataframe from HTML table")
    def get_dataframe_from_html_table(self):
        result_table_html = self.get_result_table().get_attribute('outerHTML')
        dfs = pd.read_html(result_table_html)
        df = dfs[0]
        return df

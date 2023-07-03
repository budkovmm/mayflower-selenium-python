import logging
import pytest
import allure

from src.models.customer import Customer
from src.pages.trysql.page import TrySQL
from src.utils.data_generator import generate_random_customer
from src.utils.sql_builder import CustomersSqlBuilder

from assertpy import assert_that, soft_assertions

NO_RESULT = "No result."


@pytest.mark.usefixtures("setup")
class TestCustomers:
    logger = logging.getLogger()
    query_builder = CustomersSqlBuilder()

    @allure.description(
        "Check that row with ContactNamt = 'Giovanni Rovelli' having Address = 'Via Ludovico il Moro 22'")
    def test_giovanni_rovelli_address(self):
        expected_contact_name = "Giovanni Rovelli"
        expected_address = "Via Ludovico il Moro 22"

        homepage = TrySQL(self.driver)
        homepage.open()
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        self.logger.info(df.to_string())

        assert_that(self.check_column_exist(df, "ContactName")).is_true()

        is_expected_contact_name_exist = df.loc[df['ContactName'] == expected_contact_name].any().all()
        assert_that(is_expected_contact_name_exist).is_true()

        series = df.loc[df['ContactName'] == expected_contact_name]
        actual_address = series["Address"].values[0]
        assert_that(actual_address).is_equal_to(expected_address)

    @allure.description("Check that exist 6 rows in the table where City = 'London'")
    def test_customers_from_london(self):
        expected_length_of_rows = 6

        homepage = TrySQL(self.driver)
        homepage.open()
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        london_city_df = df.loc[(df['City'] == "London")]
        self.logger.info(london_city_df.to_string())

        assert_that(london_city_df.index).is_length(expected_length_of_rows)

    @allure.description("Check that user can insert new Customer row to the table")
    def test_insert(self):
        homepage = TrySQL(self.driver)
        homepage.open()
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        max_customer_id_before = df["CustomerID"].max()

        new_customer = generate_random_customer(max_customer_id_before + 1)
        homepage.fill_query_form(self.query_builder.insert(new_customer))
        homepage.run_sql()

        homepage.fill_query_form(self.query_builder.select_by_customer_id(new_customer))
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        assert_that(df.index).is_length(1)
        customer_data = df.loc[0]

        self.validate_customer(customer_data, new_customer)

    @allure.description("Check that user can update existed Customer row in the table")
    def test_update(self):
        homepage = TrySQL(self.driver)
        homepage.open()
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        customer_id = df["CustomerID"].max()

        updated_customer = generate_random_customer(customer_id)
        homepage.fill_query_form(self.query_builder.update_by_customer_id(updated_customer))
        homepage.run_sql()

        homepage.fill_query_form(self.query_builder.select_by_customer_id(updated_customer))
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_not_equal_to(NO_RESULT)

        df = homepage.get_dataframe_from_html_table()
        assert_that(df.index).is_length(1)
        customer_data = df.loc[0]

        self.validate_customer(customer_data, updated_customer)

    @allure.description("Check that user can delete existed Customer row from the table")
    def test_delete(self):
        homepage = TrySQL(self.driver)
        homepage.open()
        homepage.run_sql()

        df = homepage.get_dataframe_from_html_table()
        customer_id = df["CustomerID"].max()

        updated_customer = generate_random_customer(customer_id)
        homepage.fill_query_form(self.query_builder.delete_by_customer_id(updated_customer))
        homepage.run_sql()

        homepage.fill_query_form(self.query_builder.select_by_customer_id(updated_customer))
        homepage.run_sql()

        assert_that(homepage.get_result_text()).is_equal_to(NO_RESULT)

    @staticmethod
    def check_column_exist(df, column_name: str):
        if column_name in df.columns:
            return True
        return False

    @staticmethod
    def validate_customer(customer_data, customer: Customer):
        with soft_assertions():
            assert_that(customer_data["CustomerID"]).is_equal_to(customer.id)
            assert_that(customer_data["CustomerName"]).is_equal_to(customer.name)
            assert_that(customer_data["ContactName"]).is_equal_to(customer.contact_name)
            assert_that(customer_data["Address"]).is_equal_to(customer.address)
            assert_that(customer_data["City"]).is_equal_to(customer.city)
            assert_that(customer_data["PostalCode"]).is_equal_to(customer.postal_code)
            assert_that(customer_data["Country"]).is_equal_to(customer.country)

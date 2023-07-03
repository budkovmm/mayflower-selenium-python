from pypika import Table, Query

from src.models.customer import Customer


class CustomersSqlBuilder:
    customers = Table('Customers')

    def select_all(self):
        query = (
            Query.from_(self.customers)
            .select(self.customers.star)
        )

        return self._prepare_query(query)

    def select_by_customer_id(self, customer: Customer):
        query = (
            Query.from_(self.customers)
            .select(self.customers.star)
            .where(self.customers.CustomerID == customer.id)
        )

        return self._prepare_query(query)

    def insert(self, customer: Customer):
        query = (
            Query.into(self.customers)
            .columns(
                self.customers.CustomerID,
                self.customers.CustomerName,
                self.customers.ContactName,
                self.customers.Address,
                self.customers.City,
                self.customers.PostalCode,
                self.customers.Country
            )
            .insert(
                customer.id,
                customer.name,
                customer.contact_name,
                customer.address,
                customer.city,
                customer.postal_code,
                customer.country
            )
        )

        return self._prepare_query(query)

    def update_by_customer_id(self, customer: Customer):
        query = (
            self.customers.update()
            .set(self.customers.CustomerName, customer.name)
            .set(self.customers.ContactName, customer.contact_name)
            .set(self.customers.Address, customer.address)
            .set(self.customers.City, customer.city)
            .set(self.customers.PostalCode, customer.postal_code)
            .set(self.customers.Country, customer.country)
            .where(self.customers.CustomerID == customer.id)
        )
        return self._prepare_query(query)

    def delete_by_customer_id(self, customer: Customer):
        query = (
            Query.from_(self.customers)
            .delete()
            .where(self.customers.CustomerID == customer.id)
        )
        return self._prepare_query(query)

    @staticmethod
    def _prepare_query(query):
        sql = query.get_sql()
        formatted_sql = sql.replace("\"", "").replace("\n", " ").replace("\r", " ")
        return formatted_sql

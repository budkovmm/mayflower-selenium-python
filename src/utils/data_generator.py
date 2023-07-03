from faker import Faker

from src.models.customer import Customer


def generate_random_customer(customer_id: int) -> Customer:
    fake = Faker()
    address = fake.address().replace("\n", " ").replace("\r", " ")

    return Customer(
        id=customer_id,
        name=fake.name(),
        contact_name=fake.name(),
        address=address,
        city=fake.city(),
        postal_code=int(fake.postcode()),
        country=fake.country()
    )

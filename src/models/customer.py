from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    name: str
    contact_name: str
    address: str
    city: str
    postal_code: int
    country: str

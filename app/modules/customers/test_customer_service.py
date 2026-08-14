import pytest

from app.core.exceptions import ConflictException
from app.modules.customers.models import Customer
from app.modules.customers.schemas import CustomerCreate


@pytest.mark.asyncio
async def test_create_customer():
    """
    Test customer creation through the service layer.
    """

    class FakeRepository:
        async def get_by_national_id(
            self,
            national_id: str,
        ):
            return None

        async def get_by_phone_number(
            self,
            phone_number: str,
        ):
            return None

        async def create(
            self,
            customer: Customer,
        ):
            customer.id = 1
            return customer

    class FakeSession:
        def add(self, obj):
            pass

        async def flush(self):
            pass

        async def refresh(self, obj):
            pass

        async def commit(self):
            pass

    from app.modules.customers.service import (
        CustomerService,
    )

    service = CustomerService(
        FakeSession()
    )

    service.repository = FakeRepository()

    data = CustomerCreate(
        national_id="1234567890",
        first_name="Ali",
        last_name="Ahmadi",
        phone_number="09121234567",
    )

    customer = await service.create_customer(
        data
    )

    assert customer.id == 1
    assert customer.first_name == "Ali"
    assert customer.last_name == "Ahmadi"


@pytest.mark.asyncio
async def test_duplicate_national_id():
    """
    Test that duplicate national IDs are rejected.
    """

    class FakeRepository:
        async def get_by_national_id(
            self,
            national_id: str,
        ):
            return Customer(
                id=1,
                national_id=national_id,
                first_name="Ali",
                last_name="Ahmadi",
                phone_number="09121234567",
            )

        async def get_by_phone_number(
            self,
            phone_number: str,
        ):
            return None

    class FakeSession:
        pass

    from app.modules.customers.service import (
        CustomerService,
    )

    service = CustomerService(
        FakeSession()
    )

    service.repository = FakeRepository()

    data = CustomerCreate(
        national_id="1234567890",
        first_name="Reza",
        last_name="Ahmadi",
        phone_number="09123333333",
    )

    with pytest.raises(ConflictException):
        await service.create_customer(data)
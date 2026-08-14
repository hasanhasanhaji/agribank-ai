from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerUpdate,
)


class CustomerService:
    """
    Implement customer-related business logic.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.repository = CustomerRepository(session)

    async def create_customer(
        self,
        data: CustomerCreate,
    ) -> Customer:
        """
        Create a new customer.
        """

        existing_customer = (
            await self.repository.get_by_national_id(
                data.national_id
            )
        )

        if existing_customer:
            raise ConflictException(
                message=(
                    "A customer with this national "
                    "ID already exists."
                )
            )

        existing_phone = (
            await self.repository.get_by_phone_number(
                data.phone_number
            )
        )

        if existing_phone:
            raise ConflictException(
                message=(
                    "A customer with this phone "
                    "number already exists."
                )
            )

        customer = Customer(
            national_id=data.national_id,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
        )

        await self.repository.create(customer)

        await self.session.commit()

        return customer

    async def get_customer(
        self,
        customer_id: int,
    ) -> Customer:
        """
        Retrieve a customer by ID.
        """

        customer = await self.repository.get_by_id(
            customer_id
        )

        if customer is None:
            raise NotFoundException(
                message="Customer not found."
            )

        return customer

    async def list_customers(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[Customer], int, int]:
        """
        Retrieve a paginated list of customers.
        """

        offset = (page - 1) * page_size

        customers = await self.repository.get_all(
            offset=offset,
            limit=page_size,
        )

        total = await self.repository.count()

        total_pages = (
            ceil(total / page_size)
            if total > 0
            else 0
        )

        return customers, total, total_pages

    async def update_customer(
        self,
        customer_id: int,
        data: CustomerUpdate,
    ) -> Customer:
        """
        Update an existing customer.
        """

        customer = await self.get_customer(
            customer_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "phone_number" in update_data:
            existing_phone = (
                await self.repository.get_by_phone_number(
                    update_data["phone_number"]
                )
            )

            if (
                existing_phone
                and existing_phone.id != customer.id
            ):
                raise ConflictException(
                    message=(
                        "This phone number is already "
                        "assigned to another customer."
                    )
                )

        for field, value in update_data.items():
            setattr(customer, field, value)

        await self.session.commit()

        await self.session.refresh(customer)

        return customer

    async def delete_customer(
        self,
        customer_id: int,
    ) -> None:
        """
        Delete a customer.
        """

        customer = await self.get_customer(
            customer_id
        )

        await self.repository.delete(customer)

        await self.session.commit()
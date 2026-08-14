from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customers.models import Customer


class CustomerRepository:
    """
    Handle database operations related to customers.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_by_id(
        self,
        customer_id: int,
    ) -> Customer | None:
        """
        Retrieve a customer by ID.
        """

        result = await self.session.execute(
            select(Customer).where(
                Customer.id == customer_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_national_id(
        self,
        national_id: str,
    ) -> Customer | None:
        """
        Retrieve a customer by national ID.
        """

        result = await self.session.execute(
            select(Customer).where(
                Customer.national_id == national_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_phone_number(
        self,
        phone_number: str,
    ) -> Customer | None:
        """
        Retrieve a customer by phone number.
        """

        result = await self.session.execute(
            select(Customer).where(
                Customer.phone_number == phone_number
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        offset: int,
        limit: int,
    ) -> list[Customer]:
        """
        Retrieve a paginated list of customers.
        """

        result = await self.session.execute(
            select(Customer)
            .order_by(Customer.id)
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        """
        Return the total number of customers.
        """

        result = await self.session.execute(
            select(func.count()).select_from(Customer)
        )

        return result.scalar_one()

    async def create(
        self,
        customer: Customer,
    ) -> Customer:
        """
        Persist a new customer.
        """

        self.session.add(customer)

        await self.session.flush()

        await self.session.refresh(customer)

        return customer

    async def delete(
        self,
        customer: Customer,
    ) -> None:
        """
        Delete a customer from the database.
        """

        await self.session.delete(customer)
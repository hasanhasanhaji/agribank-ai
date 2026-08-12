from sqlalchemy import select
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
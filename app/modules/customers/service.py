from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import CustomerCreate

class CustomerService:
    """
    Implement customer-related business logic.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.repository = CustomerRepository(session)
        self.session = session

    async def create_customer(
        self,
        data: CustomerCreate,
    ) -> Customer:
        """
        Create a new customer after validating
        business-level constraints.
        """

        existing_customer = (
            await self.repository.get_by_national_id(
                data.national_id
            )
        )

        if existing_customer:
            raise ValueError(
                "A customer with this national ID "
                "already exists."
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
    ) -> Customer | None:
        """
        Retrieve a customer by ID.
        """

        return await self.repository.get_by_id(
            customer_id
        )
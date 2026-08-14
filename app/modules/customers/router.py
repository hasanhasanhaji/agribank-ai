from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
)
from app.modules.customers.service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    data: CustomerCreate,
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """
    Create a new bank customer.
    """

    service = CustomerService(session)

    return await service.create_customer(data)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """
    Retrieve a customer by ID.
    """

    service = CustomerService(session)

    return await service.get_customer(customer_id)


@router.get(
    "",
    response_model=CustomerListResponse,
)
async def list_customers(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page",
    ),
    session: AsyncSession = Depends(get_db),
) -> CustomerListResponse:
    """
    Retrieve a paginated list of customers.
    """

    service = CustomerService(session)

    customers, total, total_pages = (
        await service.list_customers(
            page=page,
            page_size=page_size,
        )
    )

    return CustomerListResponse(
        items=customers,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """
    Partially update a customer.
    """

    service = CustomerService(session)

    return await service.update_customer(
        customer_id=customer_id,
        data=data,
    )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a customer.
    """

    service = CustomerService(session)

    await service.delete_customer(customer_id)
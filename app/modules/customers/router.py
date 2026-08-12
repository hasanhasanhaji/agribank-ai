from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session as get_db
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerResponse,
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

    try:
        customer = await service.create_customer(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return customer


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

    customer = await service.get_customer(
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer
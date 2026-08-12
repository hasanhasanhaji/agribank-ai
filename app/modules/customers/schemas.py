from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    """
    Request schema for creating a customer.
    """

    national_id: str = Field(
        min_length=10,
        max_length=10,
    )

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    phone_number: str = Field(
        min_length=10,
        max_length=20,
    )


class CustomerResponse(BaseModel):
    """
    Response schema for customer data.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    national_id: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime


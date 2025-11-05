from pydantic import BaseModel, EmailStr, Field

class OrderBase(BaseModel):
    customer_email: EmailStr
    product_name: str
    amount: float

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        from_attributes = True

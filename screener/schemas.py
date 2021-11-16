from pydantic import BaseModel, validator
from typing import Optional


class ScreenerModel(BaseModel):
    public: bool = False
    currency: Optional[str]
    market_sector: Optional[str]
    region: Optional[str]
    index: Optional[str]
    market_cap: Optional[str]
    ebitda: Optional[str]
    debt_equity: Optional[str]
    p_e: Optional[str]
    roa: Optional[str]
    roe: Optional[str]
    beta: Optional[str]
    revenue: Optional[str]
    debt: Optional[str]
    expenses: Optional[str]
    price: Optional[str]

    @validator('currency')
    def check_currency(cls, value):
        if value == 'USD':
            return value
        else:
            raise ValueError('USD currency is only available')

    class Config:
        orm_mode = True


class ShareScreenerModel(BaseModel):
    public: bool

    class Config:
        orm_mode = True

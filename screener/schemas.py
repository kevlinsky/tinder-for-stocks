from pydantic import BaseModel, validator
from typing import Optional
import re


class ScreenerModel(BaseModel):
    public: bool = False
    currency: Optional[str]
    market_sector: Optional[str]
    region: Optional[str]
    exchange: Optional[str]
    market_cap: Optional[str]
    ebitda: Optional[str]
    debt_equity: Optional[str]
    p_e: Optional[str]
    roa: Optional[str]
    roe: Optional[str]
    beta: Optional[str]
    revenue: Optional[str]
    debt: Optional[str]
    price: Optional[str]

    class Config:
        orm_mode = True

    @validator('currency')
    def check_currency(cls, value):
        if value:
            if value == "USD":
                return value
            else:
                raise ValueError('Wrong currency')
        else:
            return value

    @validator('market_sector')
    def check_market_sector(cls, value):
        if value:
            sectors_available = ['FINANCE', 'TECHNOLOGY', 'TRADE & SERVICES', 'MANUFACTURING', 'LIFE SCIENCES',
                                 'ENERGY & TRANSPORTATION', 'REAL ESTATE & CONSTRUCTION']
            sectors = set(value.split(', '))
            if sectors.issubset(sectors_available):
                return value
            else:
                raise ValueError('Wrong market sector')
        else:
            return value

    @validator('market_cap', 'ebitda', 'debt_equity', 'p_e', 'roa', 'roe', 'beta', 'revenue', 'debt', 'price')
    def check_interval_field(cls, value):
        if value:
            values = value.split(' - ')
            if re.match(r"^(-?\d+(\.\d+)?) - (-?\d+(\.\d+)?)$", value) and (values[0] < values[1]):
                return value
            else:
                raise ValueError('Wrong data input for interval fields')
        else:
            return value


class ShareScreenerModel(BaseModel):
    public: bool

    class Config:
        orm_mode = True

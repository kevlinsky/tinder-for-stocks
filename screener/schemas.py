from pydantic import BaseModel, validator


class ScreenerModel(BaseModel):
    public: bool = False
    currency: str = ''
    market_sector: str = ''
    region: str = ''
    index: str = ''
    market_cap: str = ''
    ebitda: str = ''
    debt_equity: str = ''
    p_e: str = ''
    roa: str = ''
    roe: str = ''
    beta: str = ''
    revenue: str = ''
    debt: str = ''
    expenses: str = ''
    price: str = ''

    @validator('currency')
    def check_currency(cls, value):
        if (value == '') | (value == 'USD'):
            return value
        else:
            raise ValueError('USD currency is only available')

    class Config:
        orm_mode = True


class ShareScreenerModel(BaseModel):
    public: bool

    class Config:
        orm_mode = True

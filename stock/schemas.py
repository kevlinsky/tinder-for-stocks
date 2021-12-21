from pydantic import BaseModel
import decimal


class StockModel(BaseModel):
    id: int
    market_link: str
    currency: str
    market_sector: str
    region: str
    exchange: str
    market_cap: decimal.Decimal
    ebitda: decimal.Decimal
    debt_equity: decimal.Decimal
    p_e: decimal.Decimal
    roa: decimal.Decimal
    roe: decimal.Decimal
    beta: decimal.Decimal
    revenue: decimal.Decimal
    debt: decimal.Decimal
    price: decimal.Decimal
    figi: str

    class Config:
        orm_mode = True
        json_encoders = {decimal.Decimal: str}
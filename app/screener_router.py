from typing import List

from fastapi import APIRouter

from stock.schemas import StockModel
from user.auth import Auth
from user.models import User
from screener.schemas import ScreenerModel, ShareScreenerModel
from user.models import UserScreener
from screener.models import Screener
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security, HTTPException
from screener.filter import filter_stocks

router = APIRouter(prefix="/screener", tags=["screeners"])
auth_handler = Auth()
security = HTTPBearer()


@router.post('/')
async def create_screener(screener_details: ScreenerModel,
                          credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    if user.is_active:
        screener_id = await Screener.create(owner_id=user.id,
                                            public=screener_details.public,
                                            currency=screener_details.currency,
                                            market_sector=screener_details.market_sector,
                                            region=screener_details.region,
                                            exchange=screener_details.exchange,
                                            market_cap=screener_details.market_cap,
                                            ebitda=screener_details.ebitda,
                                            debt_equity=screener_details.debt_equity,
                                            p_e=screener_details.p_e,
                                            roa=screener_details.roa,
                                            roe=screener_details.roe,
                                            beta=screener_details.beta,
                                            revenue=screener_details.revenue,
                                            debt=screener_details.debt,
                                            price=screener_details.price)
        user_screener = await UserScreener.create(user_id=user.id, screener_id=screener_id)
        if user_screener:
            return {'id': screener_id, "message": "screener was successfully created"}
        else:
            await Screener.delete(screener_id)
            raise HTTPException(status_code=501, detail='Screener is not created')
    else:
        raise HTTPException(status_code=403, detail='Verify your email')


@router.get('/', response_model=List[ScreenerModel])
async def get_user_screeners(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    screeners = await Screener.get_user_screeners(user.id)
    return screeners


@router.get('/{screener_id}', response_model=List[StockModel])
async def run_screener(screener_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    screener = await Screener.get(screener_id)
    if screener:
        if (screener.owner_id == user.id) | screener.public:
            result = await filter_stocks(screener)
            return result
        else:
            raise HTTPException(status_code=404, detail='Not found')
    else:
        raise HTTPException(status_code=404, detail='Not found')


@router.patch('/{screener_id}')
async def update_screener(screener_id: int, screener_details: ScreenerModel,
                          credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    screener = await Screener.get(id=screener_id)
    screener_dict = screener_details.dict()
    update_fields = {k: v for k, v in screener_dict.items() if v is not None}
    if screener:
        if screener.owner_id == user.id:
            await Screener.update(screener_id, **update_fields)
            return {'message': f"screener {screener_id} was successfully updated"}
        else:
            raise HTTPException(status_code=403, detail='Sorry, you can update only your own screeners')
    else:
        raise HTTPException(status_code=404, detail='Not found')


@router.delete('/{screener_id}')
async def delete_screener(screener_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    screener = await Screener.get(id=screener_id)
    if screener:
        if screener.owner_id == user.id:
            await Screener.delete(screener_id)
            return {'message': f'Screener {screener_id} was successfully deleted'}
        else:
            raise HTTPException(status_code=403, detail='Sorry, you can delete only your own screeners')
    else:
        raise HTTPException(status_code=404, detail='Not found')


@router.patch('/{screener_id}/share')
async def share_screener(screener_id: int, screener_share: ShareScreenerModel,
                         credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email = auth_handler.decode_token(token)
    user = await User.get_by_email(email)
    screener = await Screener.get(id=screener_id)
    if screener:
        if screener.owner_id == user.id:
            await Screener.update(screener_id,
                                  public=screener_share.public)
            if screener.public:
                return {'message': f'Screener {screener_id} can be used by others now'}
            else:
                return {'message': f'Screener {screener_id} can not be used by others now'}
        else:
            raise HTTPException(status_code=403, detail='Sorry, you can share only your own screeners')
    raise HTTPException(status_code=404, detail='Not found')

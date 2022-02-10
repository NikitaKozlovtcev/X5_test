import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.api import crud_data

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/data")
async def get_data(n: Optional[int] = Query(..., gt=0)):
    """
    - возвращает JSON с последними n записями из БД где n - передается в get-параметре запроса

    :param n: count of row from database to response

    :return: JSON with n row from database
    """
    exist = await crud_data.get(limit=n)
    return exist

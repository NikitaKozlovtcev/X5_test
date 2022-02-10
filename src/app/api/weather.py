import logging
from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from app.api import crud_weather
from app.api.weather_apis import get_weather, URLS

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/weather")
async def weather_on_moscow(user_agent: Optional[str] = Header(None), timeout: Optional[float] = 2.0):
    """
    - принимать запрос типа GET от пользователя, фиксировать детали запроса (заголовки, время запроса) в БД
    - запросить погоду в москве  возвращать в виде JSON включающий время ответа и температуру воздуха (время в UTC)
    - в случае успешного запроса по погоде - обновлять запись в БД - добавлять информацию о температуре
    - в случае если ни один из публичных сервисов не вернул ответ - JSON ответ со статусом 200 и просьбой попробовать позже
    - В случае если обработка запроса занимает более 2 секунд - возвращать клиенту JSON ответ со статусом 200 и сообщением,
    что ресурс временно перегружен, попробуйте позже (желательно успеть сформировать ответ)

    :param user_agent: user's Headers

    :param timeout: Optional timeout to limit weather data collection time

    :return: JSON example: { "time": "2022-02-10T15:30:00",  "temperature": 2 }
    """

    # - принимать запрос типа GET от пользователя, фиксировать детали запроса (заголовки, время запроса) в БД
    weather_request_id = await crud_weather.post(user_agent)
    # - запросить погоду в москве  возвращать в виде JSON включающий время ответа и температуру воздуха (время в UTC)
    weather, t_errors = await get_weather(timeout=timeout)
    # - В случае если обработка запроса занимает более 2 секунд - возвращать клиенту JSON ответ со статусом 200 и
    #   сообщением, что ресурс временно перегружен, попробуйте позже (желательно успеть сформировать ответ)
    if t_errors >= len(URLS.keys()):
        raise HTTPException(status_code=200, detail="Ресурс временно перегружен, попробуйте позже")
    # - в случае успешного запроса по погоде - обновлять запись в БД - добавлять информацию о температуре
    if weather:
        log.warning(weather)
        await crud_weather.put(weather_request_id, weather['data']['temperature'],  weather['data']['time'])
        response = {
            "time": weather['data']['time'],
            "temperature": weather['data']['temperature'],
        }
        return response
    else:
        raise HTTPException(status_code=200, detail="Просьба попробовать позже")


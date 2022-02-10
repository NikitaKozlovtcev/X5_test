from app.db import database, weather


async def post(headers: str):
    query = weather.insert().values(headers=headers)
    return await database.execute(query=query)


async def put(id: int, temperature: float, updated_date: str):
    query = (weather.update().
             where(id == weather.c.id).
             values(temperature=temperature, updated_date=updated_date).
             returning(weather.c.id))
    return await database.execute(query=query)

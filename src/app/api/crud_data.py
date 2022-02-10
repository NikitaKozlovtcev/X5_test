from app.db import database, weather


async def get(limit: int = 5):
    query = weather.select().order_by(weather.c.id.desc()).limit(limit)
    return await database.fetch_all(query=query)

from Core.Environment.databaseServiceEnv import DATABASE_API_URL, DATABASE_SERVICE_API_KEY
from httpx import AsyncClient

articlesDatabaseClient = AsyncClient(
    base_url=DATABASE_API_URL+"/articles",
    headers={"X-API-KEY": DATABASE_SERVICE_API_KEY}
)

accountsDatabaseClient = AsyncClient(
    base_url=DATABASE_API_URL+"/accounts",
    headers={"X-API-KEY": DATABASE_SERVICE_API_KEY}
)


import json
from Core.Configuration.databaseConfiguration import articlesDatabaseClient, accountsDatabaseClient


class Database:
    @staticmethod
    async def createUser(user, accountType="user"):

        response = await accountsDatabaseClient.post(
            url="/create",
            headers=accountsDatabaseClient.headers.update({
                "account_type": accountType
            }),
            content=json.dumps(user),
        )
        return response.json()


    @staticmethod
    async def getAccountsWithFilter(user, accountType="user"):
        response = await accountsDatabaseClient.request(
            method="GET",
            url="/getAccounts",
            content=json.dumps(user),
            headers=accountsDatabaseClient.headers.update({
                "account_type": accountType
            })
        )

        return response.json()

    @staticmethod
    async def getAccountWithId(id):

        response = await accountsDatabaseClient.get(
            url=f'/{id}',
        )

        return response.json()

    @staticmethod
    async def deleteUser(user_id):
        response = await accountsDatabaseClient.delete(
            url="/delete",
            headers=accountsDatabaseClient.headers.update({
                "id": user_id
            })
        )
        return response.json()

    @staticmethod
    async def updateUser(user):
        response = await accountsDatabaseClient.put(
            url="/update",
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    async def getAllModerators():
        response = await accountsDatabaseClient.get(
            url="/moderators",
        )
        return response

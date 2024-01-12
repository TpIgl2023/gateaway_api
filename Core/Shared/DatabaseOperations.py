import json
from Core.Configuration.databaseConfiguration import articlesDatabaseClient, accountsDatabaseClient


class Database:
    @staticmethod
    async def createUser(user, accountType="user"):

        response = await accountsDatabaseClient.post(
            url="/create",
            headers=articlesDatabaseClient.headers.update({
                "account_type": accountType
            }),
            data=json.dumps(user),
        )
        return response.json()

    #TODO : Ask what is this
    @staticmethod
    async def getAccountsWithFilter(user):

        response = await accountsDatabaseClient.get(
            url="/getAccounts",
            content=json.dumps(user),
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

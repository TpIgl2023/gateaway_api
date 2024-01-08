import json
from Core.Configuration.databaseConfiguration import articlesDatabaseClient, accountsDatabaseClient


class Database:
    @staticmethod
    def createUser(user, accountType="user"):

        response = accountsDatabaseClient.post(
            url="/create",
            headers=articlesDatabaseClient.headers.update({
                "account_type": accountType
            }),
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    def getAccountsWithFilter(user):

        response = accountsDatabaseClient.get(
            url="/getAccounts",
            data=json.dumps(user),
        )

        return response.json()

    @staticmethod
    def deleteUser(user_id):
        response = accountsDatabaseClient.delete(
            url="/delete",
            headers=accountsDatabaseClient.headers.update({
                "id": user_id
            })
        )
        return response.json()

    @staticmethod
    def updateUser(user):
        response = accountsDatabaseClient.put(
            url="/update",
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    def getAllModerators():
        response = accountsDatabaseClient.get(
            url="/moderators",
        )
        return response

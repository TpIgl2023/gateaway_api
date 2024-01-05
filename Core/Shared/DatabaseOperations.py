import requests
import json
from Core.Environment.databaseServiceEnv import DATABASE_API_URL, DATABASE_SERVICE_API_KEY
class Database:
    @staticmethod
    def createUser(user, accountType="user"):
        response = requests.post(
            url=DATABASE_API_URL + "/accounts/create",
            headers={
                "account_type": accountType,
                "x-api-key": DATABASE_SERVICE_API_KEY
            },
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    def getAccountsWithFilter(user):
        response = requests.get(
            url=DATABASE_API_URL + "/accounts/getAccounts",
            headers={
                "x-api-key": DATABASE_SERVICE_API_KEY
            },
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    def deleteUser(id):
        response = requests.delete(
            url=DATABASE_API_URL + "/accounts/delete",
            headers={
                "x-api-key": DATABASE_SERVICE_API_KEY,
                "id": id
            }
        )
        return response.json()

    @staticmethod
    def updateUser(user):
        response = requests.put(
            url=DATABASE_API_URL + "/accounts/update",
            headers={
                "x-api-key": DATABASE_SERVICE_API_KEY
            },
            data=json.dumps(user),
        )
        return response.json()

    @staticmethod
    def getAllModerators():
        headers = {'x-api-key': DATABASE_SERVICE_API_KEY}
        URL = DATABASE_API_URL + "/accounts/moderators"

        return requests.get(URL, headers=headers)
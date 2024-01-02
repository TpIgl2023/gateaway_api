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
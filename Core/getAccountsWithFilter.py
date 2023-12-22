import requests
import json
from env import DATABASE_API_URL , DATABASE_SERVICE_API_KEY
def getAccountsWithFilter(user):
    #try:
        response = requests.get(
            url=DATABASE_API_URL + "/accounts/getAccounts",
            headers={
                "x-api-key": DATABASE_SERVICE_API_KEY
            },
            data=json.dumps(user),
        )
        return response.json()
    #except Exception as e:
    #    return {
    #        "message": "Error while sending request to database-service",
    #        "error": str(e)
    #    }
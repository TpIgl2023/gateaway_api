import requests
import json
from Core.Environment.env import DATABASE_API_URL , DATABASE_SERVICE_API_KEY
def createUser(user):
    #try:
        response = requests.post(
            url=DATABASE_API_URL + "/accounts/create",
            headers= {
                "account_type" : "user",
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
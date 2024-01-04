from urllib.parse import urlparse

from starlette.responses import JSONResponse

from Core.Shared.DatabaseOperations import Database


def is_url(input_string):
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False

def isModerator(id):
    response = Database.getAllModerators()
    if response.status_code != 200:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while getting moderators",
                "error": "getting all moderators returned 404 status code , check if the database-service is running"
            })

    moderators = response.json()
    moderators = moderators["moderators"]

    isMod = False
    for moderator in moderators:
        if moderator["id"] == id:
            isMod = True
            break

    return isMod
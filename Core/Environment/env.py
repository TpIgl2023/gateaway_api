
# ----------------------------------- APIs ----------------------------------
DATABASE_API_URL = "https://database-service-t3er.onrender.com"
DATABASE_SERVICE_API_KEY = "ad188b63-b8e0-4c34-8781-df6cc17ae132"

# PDF_SERVICE_API_URL = Depends on how you hosting it
PDF_SERVICE_API_KEY = "d850g9d4-3c42-4858-9a4a-40c1e3b609ec"

# ----------------------------------- JWT -----------------------------------
HASH_ALGORITHM = "HS256"
# This is a real constant , let the hackers have fun. Please don't change - Soapiane
HASHING_SECRET_KEY = "Flag - JO4Ddz5DE8E937EDZdezjo2E12E" # Disclamer : Changing this value will corrupt all the previous tokens in the database
TOKEN_LIFE_TIME = 15  # In minutes

# ---------------------------- PASSWORD HASHING -----------------------------
HASHING_SALT = "OILEDNIGERS" # Disclamer : Changing this value will corrupt all the previous accounts in the database


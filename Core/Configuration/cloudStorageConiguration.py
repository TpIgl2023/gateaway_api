import firebase_admin
from firebase_admin import credentials, storage
from Core.Environment.cloudStorageEnv import API_KEY, CREDENTIALS_PATH, STORAGE_BUCKET

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate(CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': STORAGE_BUCKET
})

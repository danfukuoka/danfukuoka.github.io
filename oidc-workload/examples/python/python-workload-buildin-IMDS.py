from pymongo import MongoClient

# define properties and MongoClient

app_registration_client_id = ""
managed_identity_client_id = ""

properties = {"ENVIRONMENT": "azure", "TOKEN_RESOURCE": app_registration_client_id}
client = MongoClient(
    "mongodb+srv://cluster0.xxxx.mongodb.net",
    username=managed_identity_client_id, # Managed Identity_Client ID
    authMechanism="MONGODB-OIDC",
    authMechanismProperties=properties
)

# List databases to confirm connection
print(properties)
try:
    databases = client.list_database_names()
    print("Databases:", databases)
except Exception as e:
    print("Error connecting to MongoDB Atlas:", e)
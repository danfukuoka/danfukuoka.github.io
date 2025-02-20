from pymongo import MongoClient

# define properties and MongoClient

app_registration_client_id = "9d5ea4c4-42b0-46de-8ecc-1b9f51xxxxxx"
managed_identity_client_id = "d230a4f2-9e23-4576-a47f-ebb0e20xxxxx"

properties = {"ENVIRONMENT": "azure", "TOKEN_RESOURCE": app_registration_client_id}
client = MongoClient(
    "mongodb+srv://cluster0.cwfdw.mongodb.net",
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
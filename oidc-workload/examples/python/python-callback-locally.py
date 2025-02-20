from azure.identity import ClientSecretCredential
from pymongo import MongoClient
from pymongo.auth_oidc import OIDCCallback, OIDCCallbackContext, OIDCCallbackResult

# Define client ID, client secret, and tenant ID
app_registration_client_id = ""
app_registration_client_secret = ""
tenant_id = ""

connection_string = "mongodb+srv://cluster0.cwfdw.mongodb.net"

class MyCallback(OIDCCallback):
    def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
        credential = ClientSecretCredential(tenant_id, app_registration_client_id, app_registration_client_secret)
        token = credential.get_token(f"{app_registration_client_id}/.default").token
        print(token)
        return OIDCCallbackResult(access_token=token)
    
properties = {"OIDC_CALLBACK": MyCallback()}

client = MongoClient(
   connection_string,
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

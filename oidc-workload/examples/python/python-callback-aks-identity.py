#need to assign the identity to the VM yet.

from pymongo import MongoClient
from azure.identity import DefaultAzureCredential
from pymongo.auth_oidc import OIDCCallback, OIDCCallbackContext, OIDCCallbackResult
         
# define callback, properties, and MongoClient
app_registration_client_id = ""
connection_string = ""

class MyCallback(OIDCCallback):
    def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
        #credential = DefaultAzureCredential(managed_identity_client_id=managed_identity_client_id)
        credential = DefaultAzureCredential()
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


#tests
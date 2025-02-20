#need to assign the identity to the VM yet.

from pymongo import MongoClient
from azure.identity import DefaultAzureCredential
from pymongo.auth_oidc import OIDCCallback, OIDCCallbackContext, OIDCCallbackResult
         
# define callback, properties, and MongoClient
app_registration_client_id = "9d5ea4c4-42b0-46de-8ecc-1b9f5xxxxxx"
connection_string = "mongodb+srv://cluster0.cxxxxw.mongodb.net"

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


#eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImltaTBZMnowZFlLeEJ0dEFxS19UdDVoWUJUayJ9.eyJhdWQiOiI5ZDVlYTRjNC00MmIwLTQ2ZGUtOGVjYy0xYjlmNTExYWNlZDQiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vOGNjMzlkY2YtNTdlNC00NDg1LTgzODUtOTlmYzY5YTkwY2M2L3YyLjAiLCJpYXQiOjE3Mzk0NzMyMDksIm5iZiI6MTczOTQ3MzIwOSwiZXhwIjoxNzM5NTU5OTA5LCJhaW8iOiJBU1FBMi84WkFBQUF5cmpSU1lCSldwc0dtNUlZRnYyTXg0SGo0TnhuUXFkZTlyZmhSUlQrVFp3PSIsImF6cCI6ImQyMzBhNGYyLTllMjMtNDU3Ni1hNDdmLWViYjBlMjA0ZGJlOCIsImF6cGFjciI6IjIiLCJvaWQiOiIyMjAzN2YzZS1iYzYyLTQzOTAtYjI5Mi1lNTA5MjJjYTlmZDMiLCJyaCI6IjEuQURRQXo1M0RqT1JYaFVTRGhabjhhYWtNeHNTa1hwMndRdDVHanN3Ym4xRWF6dFJRQVFBMEFBLiIsInN1YiI6IjIyMDM3ZjNlLWJjNjItNDM5MC1iMjkyLWU1MDkyMmNhOWZkMyIsInRpZCI6IjhjYzM5ZGNmLTU3ZTQtNDQ4NS04Mzg1LTk5ZmM2OWE5MGNjNiIsInV0aSI6Ikstcjk4b1gweUVPaWVYbTlMSE9HQUEiLCJ2ZXIiOiIyLjAifQ.BXn1SrKr12KeUs5tlG0braXCdz9ai4zELJlaPeddC2TsVeOZFOcqL_dDV3xVWNyjz7SZt6dfh2uiYyDxfCgxqvCrswo8_S1g5n4HYGktO99nDiryKwyoMP0LpvDk7xBXt1FRK3yNfF1v_NRmRM4OwH6xJ2yZ0G-fFIF9iDm__whACDYL3bAdxThBTWt6Y9a3tus922JXBoJ25HB448TT4-EgDbRo5jp8LLLd8CHdhVgz8uJs6MTlzh3uQhlsChqgmqMO2PNhhNlLTjiepAVu3ZZbTgy5rRBkS5HKUOlZXgZII_sxqzVlWUYpxkgQb21zBlIOfJg4xUnU0CZTJjuDoQ


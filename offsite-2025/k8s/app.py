import pymongo
import os
import time

uri = os.environ["MONGODB_URI"]

properties = {"ENVIRONMENT": "k8s"}  # "/var/run/secrets/kubernetes.io/serviceaccount/token"
client = pymongo.MongoClient(
   uri,
   authMechanism="MONGODB-OIDC",
   authMechanismProperties=properties
)

while True:
   
   # Print the current JWT token.
   print("TOKEN: ", open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read() if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token") else "Token file not found.")
   
   # Print the secret from the database.
   print("SECRET: ", client["secret-database"]["secret-collection"].find_one().get("secret", "Key 'secret' not found"))

   # Sleep for 10 minutes.
   print("Sleeping for 10 minutes. We expect that the token will be refreshed by the kubelet and that the MongoDB driver will automatically get the new token and access the database.")
   time.sleep(600) 

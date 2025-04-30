import pymongo
import os
import time
from datetime import datetime, timezone

# ENVIRONMENT VARIABLE
uri = os.environ["MONGODB_URI"]

# DATABASE CONNECTION
properties = {"ENVIRONMENT": "k8s"}  
client = pymongo.MongoClient(
   uri,
   authMechanism="MONGODB-OIDC",
   authMechanismProperties=properties
)

# APPLICATION LOGIC
while True:
   
   # Get the current JWT token (for monitoring purposes).
   token = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read() if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token") else "Token file not found."
   
   # Print the token.
   print(f"Current Token: {token}")
   
   # Prepare the data to be inserted.
   document = {
       "timestamp": datetime.now(timezone.utc),
       "name": os.getenv('BONUSLY', 'Not Set'),
       "token": token
   }

   # Insert the document into the bonusly-k8s collection.
   client["bonusly-k8s"]["activity-log"].insert_one(document)
   print(f"Inserted document: {document}")

   print("CONGRATULATIONS! You have finished the lab. Workload Identity rocks! :)")
   
   # Sleep for 10 minutes.
   print("Sleeping for 10 minutes. We expect that the token will be refreshed by the kubelet and that the MongoDB driver will automatically get the new token and access the database.")
   time.sleep(600)
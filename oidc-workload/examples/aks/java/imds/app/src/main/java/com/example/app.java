package com.mongodb.oidc;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoCredential;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class app {
    private static final Logger logger = LoggerFactory.getLogger(app.class);

    public static void main(String[] args) {
        // Read environment variables
        String mongodbUri = System.getenv("CONNECTION_STRING");
        String managed_identity_client_id = System.getenv("MANAGED_IDENTITY_CLIENT_ID");
        String app_registration_client_id = System.getenv("APP_REGISTRATION_CLIENT_ID");

        logger.info("mongodbUri: " + mongodbUri);
        logger.info("managed_identity_client_id: " + managed_identity_client_id);
        logger.info("app_registration_client_id: " + app_registration_client_id);

        MongoCredential credential = MongoCredential.createOidcCredential(managed_identity_client_id)
                .withMechanismProperty("ENVIRONMENT", "azure")
                .withMechanismProperty("TOKEN_RESOURCE", app_registration_client_id);

        MongoClientSettings clientSettings = MongoClientSettings.builder()
                .applyConnectionString(new ConnectionString(mongodbUri))
                .credential(credential)
                .build();

        try (MongoClient mongoClient = MongoClients.create(clientSettings)) {
            MongoDatabase db = mongoClient.getDatabase("mytestdb");
            MongoCollection<Document> collection = db.getCollection("test_collection_1");

            Document document = new Document("value", "mongodb-atlas");
            collection.insertOne(document);
            logger.info("Success! Inserted ID: " + document.getObjectId("_id").toHexString());
        } catch (Exception e) {
            logger.error("An error occurred: ", e);
        }
    }
}

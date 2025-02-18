package com.mongodb.oidc;

import com.mongodb.MongoCredential;
import com.mongodb.MongoCredential.OidcCallback;
import com.mongodb.MongoCredential.OidcCallbackResult;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;
import com.mongodb.MongoClientSettings;
import com.mongodb.ConnectionString;

import java.util.Arrays;

import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder; 
import com.azure.core.credential.TokenRequestContext;

public class App {

    // Retrieve values from environment variables
    private static final String mongoURL = System.getenv("CONNECTION_STRING");
    private static final String tenantId = System.getenv("TENANT_ID");
    private static final String clientId = System.getenv("APP_REGISTRATION_CLIENT_ID");
    private static final String clientSecret = System.getenv("APP_REGISTRATION_SECRET");



    public static void main(String[] args) {

        System.out.println("CONNECTION_STRING: " + mongoURL);
        System.out.println("TENANT_ID: " + tenantId);
        System.out.println("APP_REGISTRATION_CLIENT_ID: " + clientId);
        System.out.println("APP_REGISTRATION_SECRET: " + clientSecret);

        
        try {

            // OIDC Callback implementation
            OidcCallback callback = context -> {

                // Create the ClientSecretCredential to authenticate using client credentials
                ClientSecretCredential AzureCredential = new ClientSecretCredentialBuilder()
                        .tenantId(tenantId)
                        .clientId(clientId)
                        .clientSecret(clientSecret)
                        .build();

                // Get an access token for a specific scope (e.g., Azure Management)
                TokenRequestContext requestContext = new TokenRequestContext().addScopes(clientId + "/.default");

                // Retrieve the token
                String accessToken = AzureCredential.getToken(requestContext).block().getToken();

                // Print the token to verify
                System.out.println("Access Token: " + accessToken);

                return new OidcCallbackResult(accessToken);  // Returning the token as OidcCallbackResult
            };

            // Create MongoCredential using OIDC
            MongoCredential credential = MongoCredential.createOidcCredential(null)
                .withMechanismProperty("OIDC_CALLBACK", callback);  // Using the callback

            // Create MongoClient with the necessary settings
            MongoClient mongoClient = MongoClients.create(
                MongoClientSettings.builder()
                    .applyConnectionString(new ConnectionString(mongoURL))
                    .credential(credential)
                    .build());

            // Example of selecting a database
            MongoDatabase database = mongoClient.getDatabase("myDatabase");

            // Print the database names
            System.out.println("Connected to MongoDB");
            System.out.println("Database names:");
            for (String dbName : mongoClient.listDatabaseNames()) {
                System.out.println(dbName);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

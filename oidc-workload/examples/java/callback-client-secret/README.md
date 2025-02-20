# Project AKS JAVA IMD OIDC

## Introduction
The Java driver doesn't offer built-in support for all platforms. Instead, you must define a custom callback to use OIDC to authenticate from these platforms. To do so, use the "OIDC_CALLBACK" authentication property, as shown in the following code example:

For more information on how the Java driver integrates with Azure authentication, refer to the [MongoDB Java Driver Documentation - OIDC Authentication](https://www.mongodb.com/docs/drivers/java/sync/upcoming/fundamentals/enterprise-auth/#mongodb-oidc).

## Installation Instructions

To build and deploy the application, follow these steps:

### 1. Build the JAR File
First, build the JAR file using Maven. This step compiles the source code and packages it into a deployable JAR file:

```bash
cd app
mvn clean package

### 2. Build and Push Docker Image

```bash
cd imds
docker build --platform linux/amd64 -t danilofukuoka/callback-client-secret-java:latest .
docker push danilofukuoka/callback-client-secret-java:latest
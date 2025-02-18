# Project AKS JAVA IMD OIDC

## Introduction
This project enables authentication to MongoDB using the Azure Instance Metadata Service (IMDS) when running your application on an Azure VM. The MongoDB Java driver has built-in support for Azure authentication, utilizing OpenID Connect (OIDC) to facilitate secure and seamless access to MongoDB.

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
docker build --platform linux/amd64 -t danilofukuoka/imds-java:latest .
docker push danilofukuoka/imds-java:latest
# Step 1: Use an official OpenJDK image to run the application
FROM openjdk:17-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the locally built JAR into the container
COPY ./app/target/*.jar ./app.jar

# Expose the port on which the application will run
EXPOSE 8080

# Command to run the Java application
CMD ["java", "-jar", "app.jar"]

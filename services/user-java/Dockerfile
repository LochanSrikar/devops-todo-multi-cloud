# Stage 1: Builder to "bake" the JAR
FROM maven:3.9-amazoncorretto-21 AS builder
WORKDIR /app
COPY . .

 # Build JAR, skip tests for speed
RUN mvn clean package -DskipTests 

# Stage 2: Runner for the app
FROM amazoncorretto:21-alpine
WORKDIR /app

 # Copy the baked JAR
COPY --from=builder /app/target/user-service-0.0.1-SNAPSHOT.jar app.jar 

 # Run the app
CMD ["java", "-jar", "app.jar"] 
# mongodb-docker/Dockerfile
FROM mongo:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Create a directory for MongoDB data
RUN mkdir -p /data/db

# Expose the MongoDB port
EXPOSE 27017

# Start MongoDB
CMD ["mongod"]

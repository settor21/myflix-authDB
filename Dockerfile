# Dockerfile.postgresql
FROM postgres:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Expose the PostgreSQL port
EXPOSE 5432

# Copy the PostgreSQL initialization script
COPY init.sql /docker-entrypoint-initdb.d/

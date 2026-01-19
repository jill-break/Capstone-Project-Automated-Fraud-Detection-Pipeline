FROM postgres:latest

# Environment variables (Defaults)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_DB=postgres

# Copy the initialization script to the auto-run directory
COPY postgres.sql /docker-entrypoint-initdb.d/
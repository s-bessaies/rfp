

# Project Setup Guide

## Overview

This guide provides step-by-step instructions to set up and run a React and Django project using Docker. It covers configuring environment variables, setting up the frontend to communicate with the backend, and running necessary Docker commands.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Docker**: Containerization platform
- **Docker Compose**: Tool for defining and running multi-container Docker applications

## Step 1: Set Up Environment Variables

### 1.1. Navigate to the `backend` Directory

   Ensure you are in the correct directory where the backend code resides.

### 1.2. `.env` File

   - Create `.env` file in the `backend` directory.
   - Add the following environment variables:

   ```env
   IpAdress=http://<your-local-ip-address>:8000
   OPENAI_API_KEY='your-openai-key'
   MISTRAL_API_KEY='your-mistral-key'
   ```

   - Replace `<your-local-ip-address>` with your machine's IP address. This IP address will allow the frontend to communicate with the backend API.

## Step 2: Configure the Frontend (`package.json`)

### 2.1. Open the `package.json` File

   - Navigate to the `frontend` directory and open the `package.json` file.

### 2.2. Set the Proxy

   - Add or update the proxy setting in `package.json` to route API requests to your backend:

   ```json
   "proxy": "http://<your-local-ip-address>:8000"
   ```

   - Again, replace `<your-local-ip-address>` with your actual local IP address.

   **Note**: This step ensures that API calls made by your React app are correctly forwarded to your Django backend server.

## Step 3: Build and Run Docker Containers

### 3.1. Build the Docker Images

   - Run the following command in the root directory of your project to build Docker images for your services:

   ```bash
   docker-compose build
   ```

   This command prepares your application for running by building the necessary Docker images for the backend, frontend, and database services.

### 3.2. Start the Docker Containers

   - Start all services in the background (detached mode) using the following command:

   ```bash
   docker-compose up -d
   ```

   This will start your backend, frontend, and database services as defined in your `docker-compose.yml` file.

### 3.3. Apply Django Migrations

   - After the containers are up, you need to apply migrations to set up the database schema:

   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

   These commands create and apply migrations to your PostgreSQL database.

### 3.4. Run the Containers in Attached Mode

   - To view logs and interact with your services directly, run:

   ```bash
   docker-compose up
   ```

   This command runs your services in attached mode, showing live logs in your terminal.

## Additional Notes

- Ensure that Docker Toolbox or Docker Desktop is correctly configured to use the specified IP address.
- The IP address in both `.env` and `package.json` must match for the frontend and backend to communicate properly.

## Conclusion

Following these instructions will set up your development environment, allowing you to run and test your React and Django applications inside Docker containers. If you encounter any issues, double-check the IP addresses and environment variable configurations. For further assistance, refer to Docker’s official documentation or reach out to your team.


# Trial Testing Booking in Server

## Environment Setup & Configuration

This project uses Docker Compose to run the application services, including the PostgreSQL database, server, and test runner. Configuration is managed via environment variables to support multiple deployment environments such as **development** and **production**.

Environment variables are stored in `.env` files for each environment:
  - `.env` — base variables to set the environment
  - `.env.development` — variables specific to the development environment
  - `.env.production` — variables specific to the production environment
  - `.env.testing` variables specific to the testing environment
  
  The `APP_ENV` variable controls which environment config is active and is set in the `.env` file. Once this has been set, volumes and all other environmental variables are set dynamically.

## Getting Started

Follow these steps to set up and run the project locally using Docker Compose:

1. **Install Docker & Docker Compose**

   If you don’t have Docker and Docker Compose installed, follow the official installation guide here:  
   [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

2. **Clone this repository**
   Run
   ```bash
   git clone https://github.com/ielts-ops/trial-testing-booking-in-server.git
   cd trial-testing-booking-in-server
   ```

3. **Create and configure environment files**

    Copy the example environment files to your working directory by running:
    ```bash
    cp .env.example .env
    cp .env.name.example .env.development
    cp .env.name.example .env.testing
    cp .env.name.example .env.production
    ```

    Edit each .env* file to set the appropriate environment variables such as database credentials, ports, and APP_ENV.
    
    Make sure .env contains the APP_ENV variable, for example:
    ```bash**
    APP_ENV=development
    ```

4. **Start the application**

    Run Docker Compose to build and start all containers by running:
    ```
    docker-compose up --build
    ```

    This will start the database, server, and test containers configured for the environment specified in your .env file.

5. **Access the application**

    Once running, your server should be accessible on http://localhost:8000 (or the port defined in your .env files).



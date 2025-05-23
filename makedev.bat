@echo off
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="reset" goto reset
if "%1"=="seed" goto seed
if "%1"=="test" goto test

echo Unknown command: %1
goto end

:build
docker-compose up --build
goto end

:up
docker-compose up
goto end

:down
docker-compose down
goto end

:reset
docker-compose down -v
goto end

:seed
docker-compose run server python -m src.setup_db
docker-compose down
goto end

:test
set APP_ENV=testing
docker compose run --rm tests
docker-compose down
goto end

:end


@echo off
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="reset" goto reset
if "%1"=="seed" goto seed
if "%1"=="test" goto test
if "%1"=="ignore" goto ignore

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
docker compose up -d
if "%2"=="" (
    docker compose exec server python -m src.setup_db
) else (
    docker compose exec server python -m src.setup_db %2
)
docker-compose down
goto end

:test
set APP_ENV=testing
if "%2"=="" (
    docker-compose run --rm tests
) else (
    docker-compose run --rm tests pytest %2
)
docker-compose down
goto end

:ignore
git rm --cached .env
git rm --cached .env.testing
git rm --cached .env.development
git rm --cached .env.production
git rm --cached -r __pycache__/
git rm --cached *.pyc
git rm --cached -r db/private_data/
goto end

:end


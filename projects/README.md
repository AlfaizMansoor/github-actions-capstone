# Bank App

Bank App is a small Flask web application for managing bank accounts and recording account transactions. It uses MySQL for persistent storage and is packaged with Docker Compose so the application and database can be started together.

## Features

- Create accounts with a unique account ID
- Deposit funds into an account
- Withdraw funds when the account has enough balance
- Transfer funds between two accounts
- View the transaction history for an account
- Store account balances and transactions in MySQL

## Technology

- Python 3.11
- Flask and Flask-SQLAlchemy
- MySQL 8.0
- Docker and Docker Compose

## Run With Docker Compose

1. Create a `.env` file in this directory with the database settings used by both services:

	```env
	MYSQL_ROOT_PASSWORD=rootpass
	MYSQL_DATABASE=bankdb
	MYSQL_USER=bankuser
	MYSQL_PASSWORD=bankpass
	DB_HOST=db
	DB_PORT=3306
	```

2. Build and start the application and database:

	```bash
	docker compose up --build
	```

3. Open [http://localhost:5000](http://localhost:5000) in a browser.

The application waits for MySQL to accept connections before Flask starts. Database data is persisted in the `bank-app-volume` Docker volume.

To stop the services, press `Ctrl+C`. To stop them and remove the containers, run:

```bash
docker compose down
```

## How to Use

1. Enter an account ID and select **Create Account**.
2. Use **Deposit** or **Withdraw** beside an account to update its balance.
3. Complete the transfer form to move funds between two existing accounts.
4. Select **History** to view the account's recorded transactions.

## Run Locally

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Set the database environment variables, make sure a compatible MySQL database is running, and start Flask:

```bash
python bank.py
```

The development server listens on `0.0.0.0:5000`.

## Project Structure

```text
bank.py                  Flask application, models, and routes
templates/               HTML templates for accounts and history
Dockerfile               Container image definition
docker-compose.yml       Flask and MySQL services
entrypoint.sh            Waits for MySQL before starting Flask
requirements.txt         Python dependencies
```

## Note

This project is intended for learning and local development. It does not include authentication, authorization, production database migrations, or production-grade validation and security configuration. for practice only

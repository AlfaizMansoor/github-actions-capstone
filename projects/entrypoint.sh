#!/bin/sh
echo "Waiting for db..."
until nc -z db 3306; do
  sleep 2
done
echo "DB is up, starting Flask"
exec python bank.py


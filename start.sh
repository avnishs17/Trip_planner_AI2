#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 &

# Wait a moment for FastAPI to start
sleep 5

# Start Flask frontend
echo "Starting Flask frontend on port 5000..."
gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 120 flask_app:app

# Keep the script running
wait 
#!/bin/bash

# Start FastAPI
start_fastapi() {
    echo "Starting FastAPI..."
    cd backend
    uv run fastapi dev &
    FASTAPI_PID=$!
    cd ..
}

# Start Svelte
start_svelte() {
    echo "Starting Svelte..."
    cd frontend
    npm run dev -- --open &
    SVELTE_PID=$!
    cd ..
}

# Function to clean up processes
cleanup() {
    echo "Terminating FastAPI and Svelte..."
    kill $FASTAPI_PID $SVELTE_PID
    exit
}

# Trap SIGINT and SIGTERM to call cleanup
trap cleanup SIGINT SIGTERM

# Start the applications
start_fastapi
start_svelte

# Wait for both processes to finish
wait $FASTAPI_PID
wait $SVELTE_PID

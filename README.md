# Simple Rate Limiter

A minimal rate-limiting application with a Python backend and a React frontend.

## Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend Setup

1. Create the React app with Vite:
   ```bash
   npm create vite@latest frontend
   ```
2. Install dependencies and start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Usage

- Start the backend and frontend.
- Access the application in your browser at the specified frontend URL.

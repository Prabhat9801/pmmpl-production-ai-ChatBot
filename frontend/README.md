# Frontend Setup Instructions

## Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Backend server running (see backend/README.md)

## Installation

No build process required! This is a pure HTML/CSS/JavaScript frontend.

## Running the Frontend

### Option 1: Using Python HTTP Server
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500` in your browser

### Option 2: Using VS Code Live Server
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### Option 3: Direct File Opening
Simply open `index.html` in your browser (CORS may need to be configured in backend)

## Configuration

Edit the `API_BASE_URL` in `app.js` if your backend is running on a different port:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Features

- **Chat Interface**: ChatGPT-style UI for natural language queries
- **Real-time Responses**: Instant AI-powered answers from your Google Sheets data
- **Data Tables**: Automatic table display when data is returned
- **Chat History**: View and reload previous conversations
- **Auto-refresh**: Backend data refreshes every 10 minutes
- **Responsive**: Works on desktop and mobile devices

## Usage

1. Make sure the backend is running (`http://localhost:8000`)
2. Open the frontend in your browser
3. Type your question about the data
4. Press Enter or click Send
5. View AI-powered responses with data tables

## Example Questions

- "Show me all purchases from last month"
- "What's the total revenue by product?"
- "How many orders were placed today?"
- "List all customers who spent more than $1000"
- "What are the top 5 selling products?"

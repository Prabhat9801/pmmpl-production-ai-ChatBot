# Backend Setup Instructions

## 🎯 Enhanced Agent System

This backend uses the **SAME enhanced agent system from the notebook** that achieved **82.1% success rate** across 56 diverse queries.

### Key Features:
✅ **7 Operation Types**: RETRIEVE, AGGREGATE, COMPARE, FEASIBILITY, RANK, TREND, PREDICT  
✅ **Column Aliasing**: Smart mapping of user-friendly terms to actual column names  
✅ **Date Resolution**: Handles "last 30 days", "this month", etc.  
✅ **Numeric Normalization**: Automatic type detection and conversion  
✅ **Safe Query Execution**: Error handling with fallback  
✅ **Product Grouping**: Aggregates by product for accurate results  
✅ **Qty × Rate Calculations**: Supports complex VALUE calculations  

## Prerequisites
- Python 3.8+
- pip

## Installation

1. **Create and activate virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Fill in your actual values:
     - `GOOGLE_SHEETS_CREDENTIALS_PATH`: Path to your Google service account JSON file
     - `GOOGLE_SHEET_NAME`: Name of your Google Sheet
     - `GROQ_API_KEY`: Your Groq API key

4. **Run the server:**
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### GET /health
Check system health and data refresh status

### POST /chat
Send a question and get AI-powered response
```json
{
  "question": "Show me all purchases from last month"
}
```

### GET /history
Get chat history with pagination
- Query params: `limit`, `offset`

### DELETE /history/{chat_id}
Delete a specific chat from history

### DELETE /history
Clear all chat history

### POST /refresh
Manually trigger data refresh

## Auto-Refresh
Google Sheets data automatically refreshes every 10 minutes (configurable in `.env`)

## Documentation
Interactive API docs available at: `http://localhost:8000/docs`

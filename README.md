# AI Data Assistant - Full Stack Application

A production-ready ChatGPT-style interface for querying Google Sheets data using natural language, powered by FastAPI and Groq LLaMA.

## 📁 Project Structure

```
Produnction 5/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agent.py             # Google Sheets + Groq LLM agent
│   ├── database.py          # SQLite database (Supabase-ready)
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── README.md            # Backend documentation
│
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── style.css            # ChatGPT-style CSS
│   ├── app.js               # Frontend JavaScript
│   └── README.md            # Frontend documentation
│
└── Untitled50.ipynb         # Original notebook (82.1% success rate)
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your credentials

# Run server
python main.py
```

Backend runs at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Option 1: Python HTTP Server
python -m http.server 5500

# Option 2: VS Code Live Server
# Right-click index.html → "Open with Live Server"
```

Frontend runs at: `http://localhost:5500`

## ✨ Features

### Backend
- ✅ **FastAPI REST API** with auto-generated docs
- ✅ **Google Sheets Integration** with auto-refresh every 10 minutes
- ✅ **Groq LLaMA 3.3 70B** for natural language processing
- ✅ **SQLite Database** for chat history (Supabase-ready schema)
- ✅ **CORS Enabled** for frontend communication
- ✅ **Background Tasks** for non-blocking data refresh
- ✅ **Health Monitoring** endpoint
- ✅ **82.1% Query Success Rate** (tested on 56 diverse queries)

### Frontend
- ✅ **ChatGPT-Style UI** - Clean, modern interface
- ✅ **Real-time Chat** - Instant AI responses
- ✅ **Data Tables** - Automatic table display for query results
- ✅ **Chat History** - View and reload previous conversations
- ✅ **Status Indicator** - Live system health monitoring
- ✅ **Responsive Design** - Works on all devices
- ✅ **Typing Indicators** - Shows when AI is processing

## 🔧 Configuration

### Backend (.env)
```env
GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_SHEET_NAME=Your Sheet Name
GROQ_API_KEY=your_groq_api_key
SHEETS_REFRESH_INTERVAL_MINUTES=10
DATABASE_URL=sqlite:///./chat_history.db
```

### Frontend (app.js)
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | System health check |
| POST | `/chat` | Send question, get AI response |
| GET | `/history` | Get chat history (paginated) |
| DELETE | `/history/{id}` | Delete specific chat |
| DELETE | `/history` | Clear all history |
| POST | `/refresh` | Manual data refresh |
| GET | `/docs` | Interactive API documentation |

## 🎯 Example Usage

### Chat Examples
```
"Show me all purchases from last month"
"What's the total revenue by product?"
"How many orders were placed today?"
"List customers who spent more than $1000"
"What are the top 5 selling products?"
```

### API Call Example
```javascript
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: "Show me total sales" })
})
```

## 🔄 Auto-Refresh Feature

- Google Sheets data automatically refreshes every **10 minutes**
- Refresh happens in **background** without affecting frontend
- Configurable via `SHEETS_REFRESH_INTERVAL_MINUTES`
- Manual refresh available via `/refresh` endpoint

## 💾 Database Schema (Supabase-Ready)

```sql
chat_history:
  - id (INTEGER PRIMARY KEY)
  - session_id (STRING, nullable)
  - user_question (TEXT)
  - bot_response (TEXT)
  - confidence (FLOAT)
  - rows_found (INTEGER)
  - query_type (STRING)
  - timestamp (DATETIME)
  - metadata_json (TEXT, for future extensions)
```

## 🎨 UI Design

The frontend follows ChatGPT's design principles:
- Clean, centered layout
- Smooth animations
- Typing indicators
- Message history
- Data table display
- Confidence badges
- Responsive design

## 🔐 Security Notes

- Store credentials in `.env` (never commit to git)
- Enable CORS only for trusted origins
- Use HTTPS in production
- Implement authentication if needed
- Rate limit API endpoints for production

## 🚀 Deployment Tips

### Backend
- Use **Gunicorn** or **Uvicorn** for production
- Set `RELOAD=False` in production
- Use PostgreSQL for production database
- Implement proper logging
- Add API rate limiting

### Frontend
- Deploy to **Vercel**, **Netlify**, or any static host
- Update `API_BASE_URL` to production backend
- Enable HTTPS
- Configure proper CORS origins

## 📈 System Performance

Based on comprehensive testing (56 queries):
- **Success Rate**: 82.1% (46/56 queries)
- **Operation Types**: RETRIEVE, AGGREGATE, COMPARE, FEASIBILITY, RANK, TREND, PREDICT
- **Query Categories**: 13 types covered
- **Data Scale**: 26,400+ rows across 16 sheets

## 🛠️ Technology Stack

**Backend:**
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Groq (LLaMA 3.3 70B)
- LangChain + LangGraph
- gspread (Google Sheets)
- Pandas

**Frontend:**
- Pure HTML5/CSS3/JavaScript
- No frameworks (lightweight & fast)
- Modern ES6+ JavaScript
- Responsive design

## 📝 Development

### Adding New Features

**Backend:**
1. Add endpoint in `main.py`
2. Update models in `models.py`
3. Modify agent logic in `agent.py`

**Frontend:**
1. Update UI in `index.html`
2. Add styles in `style.css`
3. Implement logic in `app.js`

### Database Migration to Supabase

The schema is already Supabase-ready:
1. Create Supabase project
2. Update `DATABASE_URL` in `.env`
3. Run migrations
4. Update database imports

## 🐛 Troubleshooting

**Backend won't start:**
- Check `.env` file exists and has correct values
- Verify Google credentials JSON file path
- Ensure all dependencies installed

**Frontend can't connect:**
- Check backend is running on correct port
- Verify `API_BASE_URL` in `app.js`
- Check browser console for CORS errors

**Data not refreshing:**
- Check `SHEETS_REFRESH_INTERVAL_MINUTES` setting
- Verify Google Sheets permissions
- Check backend logs for errors

## 📄 License

MIT License - Feel free to use for personal or commercial projects

## 🤝 Support

For issues or questions, check:
- Backend logs for errors
- Browser console for frontend issues
- `/health` endpoint for system status
- `/docs` for API documentation

---

Built with ❤️ using FastAPI, Groq LLaMA, and Google Sheets

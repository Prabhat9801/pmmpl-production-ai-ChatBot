# 🤖 PMMPL Production Management AI ChatBot

Enterprise-grade AI agent for production management. Query 16 Google Sheets using natural language with LangGraph.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Google Sheets Setup](#-google-sheets-setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Changing LLM Model](#-changing-llm-model)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Security](#-security)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **7 Operation Types** | Retrieve, Aggregate, Compare, Rank, Trend, Predict, Feasibility |
| **16 Google Sheets** | Real-time integration with production data |
| **Smart Query Routing** | Automatic intent detection using LangGraph |
| **Date Intelligence** | Understands "last 30 days", "this month", "yesterday" |
| **Self-Healing** | 2-retry mechanism for error recovery |
| **Session Management** | Chat history with session-based caching |
| **82% Accuracy** | Tested on 56+ diverse query types |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND                                   │
│                    (HTML + CSS + JavaScript)                         │
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│   │  Chat UI     │  │  Session     │  │  Markdown Renderer       │  │
│   │  Interface   │  │  Manager     │  │  (Headers, Lists, Bold)  │  │
│   └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP REST API
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           BACKEND                                    │
│                    (FastAPI + Python)                                │
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│   │  API Routes  │  │  LangGraph   │  │  Query Cache             │  │
│   │  /chat       │  │  Agent       │  │  (98% similarity)        │  │
│   │  /sessions   │  │              │  │                          │  │
│   └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│   │  Groq LLM    │  │  Google      │  │  SQLite                  │  │
│   │  LLaMA 3.3   │  │  Sheets API  │  │  Database                │  │
│   └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ gspread API
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        GOOGLE SHEETS                                 │
│                                                                      │
│   FG Stock │ Orders Pending │ RM Stock │ Daily Production │ ...     │
│                                                                      │
│                     (16 Sheets Total)                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Core language |
| FastAPI | 0.109.0 | REST API framework |
| LangGraph | 0.2.0 | AI agent orchestration |
| LangChain | 0.3.0 | LLM integration |
| Groq | Latest | LLM API provider |
| gspread | 5.12.3 | Google Sheets API |
| SQLAlchemy | 2.0.25 | Database ORM |
| Pydantic | 2.5.3 | Data validation |
| sentence-transformers | 2.7.0 | Query embeddings |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| CSS3 | Styling |
| JavaScript (ES6) | Interactivity |
| LocalStorage | Session persistence |

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed
- **Git** installed
- **Google Cloud Account** (for Google Sheets API)
- **Groq API Key** (free at https://console.groq.com)
- **Google Sheets** with your data

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Prabhat9801/pmmpl-production-ai-ChatBot.git
cd pmmpl-production-ai-ChatBot
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 📊 Google Sheets Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"**
3. Name it (e.g., `pmmpl-production-ai`)
4. Click **"Create"**

### Step 2: Enable Google Sheets API & Google Drive API

1. In your project, go to **APIs & Services** → **Library**
2. Search for **"Google Sheets API"**
3. Click on it and click **Enable**
4. Go back to **Library**
5. Search for **"Google Drive API"**
6. Click on it and click **Enable**

> ⚠️ **Important:** Both APIs must be enabled for the application to work properly. Google Drive API is required to access and list Google Sheets files.

### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **"Service Account"**
3. Fill in details:
   - Name: `pmmpl-sheets-agent`
   - Description: `Service account for Google Sheets access`
4. Click **"Create and Continue"**
5. Skip role assignment (click **"Continue"**)
6. Click **"Done"**

### Step 4: Generate JSON Key

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **JSON** format
5. Click **"Create"**
6. A `.json` file will download automatically

### Step 5: Place Credentials File

1. Rename the downloaded file to `credentials.json`
2. Place it in the `backend/` folder:
   ```
   backend/
   ├── credentials.json   ← Place here
   ├── main.py
   ├── agent.py
   └── ...
   ```

### Step 6: Share Google Sheet with Service Account

1. Open your Google Sheets file
2. Click **"Share"** button (top right)
3. Copy the **email** from your `credentials.json` file:
   ```json
   "client_email": "pmmpl-sheets-agent@your-project.iam.gserviceaccount.com"
   ```
4. Paste this email in the **"Add people"** field
5. Set permission to **"Viewer"** (read-only) or **"Editor"**
6. Uncheck **"Notify people"**
7. Click **"Share"**

### Step 7: Get Sheet Name

Copy the exact name of your Google Sheet (e.g., `Copy of PMMPL AI (Prabhat)`)

---

## ⚙️ Environment Configuration

### Step 1: Create `.env` File

Create a `.env` file in the `backend/` folder:

```bash
cd backend
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit `.env` with your actual values:

```env
# ============================================
# GOOGLE SHEETS CONFIGURATION
# ============================================

# Path to your Google credentials JSON file
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json

# Exact name of your Google Sheet (case-sensitive!)
GOOGLE_SHEET_NAME=Copy of PMMPL AI (Prabhat)

# ============================================
# API KEYS
# ============================================

# Groq API Key (get free at https://console.groq.com)
GROQ_API_KEY=gsk_your_groq_api_key_here

# LangSmith API Key (optional, for tracing)
LANGSMITH_API_KEY=lsv2_your_langsmith_key_here

# ============================================
# DATABASE
# ============================================

# SQLite database path (default)
DATABASE_URL=sqlite:///./chat_history.db

# ============================================
# SERVER CONFIGURATION
# ============================================

HOST=0.0.0.0
PORT=8000
RELOAD=True

# ============================================
# CORS SETTINGS
# ============================================

# Add your frontend URLs (comma-separated)
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500"]

# ============================================
# LLM SETTINGS
# ============================================

LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.0

# ============================================
# REFRESH SETTINGS
# ============================================

# How often to refresh Google Sheets data (in minutes)
SHEETS_REFRESH_INTERVAL_MINUTES=10
```

### Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | ✅ Yes | Path to Google credentials JSON | `credentials.json` |
| `GOOGLE_SHEET_NAME` | ✅ Yes | Name of your Google Sheet | `Copy of PMMPL AI (Prabhat)` |
| `GROQ_API_KEY` | ✅ Yes | Groq API key for LLM | `gsk_xxxx...` |
| `LANGSMITH_API_KEY` | ❌ No | LangSmith key for tracing | `lsv2_pt_xxxx...` |
| `DATABASE_URL` | ❌ No | Database connection string | `sqlite:///./chat_history.db` |
| `HOST` | ❌ No | Server host | `0.0.0.0` |
| `PORT` | ❌ No | Server port | `8000` |
| `LLM_MODEL` | ❌ No | Groq model name | `llama-3.3-70b-versatile` |
| `LLM_TEMPERATURE` | ❌ No | LLM temperature (0-1) | `0.0` |

---

## ▶️ Running the Application

### Step 1: Start Backend Server

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✅ Google Sheets connected: 16 sheets found
✅ LangGraph Agent initialized
```

### Step 2: Open Frontend

Open `frontend/index.html` in your browser:

**Option A: Direct File**
- Double-click `frontend/index.html`

**Option B: VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click `index.html` → **"Open with Live Server"**

**Option C: Python HTTP Server**
```bash
cd frontend
python -m http.server 5500
# Open: http://localhost:5500
```

### Step 3: Test the ChatBot

Try these queries:
- "Show all FG Stock"
- "How many pending orders are there?"
- "Compare Rungta and Shinghal orders"
- "Top 5 products by pending quantity"
- "When will stock run out?"

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Chat with AI
```http
POST /chat
Content-Type: application/json

{
  "question": "Show all pending orders",
  "session_id": "1234567890",
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "Here are the pending orders...",
  "confidence": 0.85,
  "rows_found": 33,
  "data_preview": [...],
  "query_type": "retrieve"
}
```

#### 2. Get Sessions
```http
GET /sessions
```

#### 3. Delete Session
```http
DELETE /sessions/{session_id}
```

#### 4. Health Check
```http
GET /health
```

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔄 Changing LLM Model

### Available Groq Models

| Model | Context | Speed | Best For |
|-------|---------|-------|----------|
| `llama-3.3-70b-versatile` | 128K | Fast | General queries (default) |
| `llama-3.1-70b-versatile` | 128K | Fast | Complex reasoning |
| `llama-3.1-8b-instant` | 128K | Very Fast | Simple queries |
| `mixtral-8x7b-32768` | 32K | Fast | Balanced performance |
| `gemma2-9b-it` | 8K | Very Fast | Quick responses |

### How to Change Model

**Option 1: Edit `.env` file**
```env
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.0
```

**Option 2: Edit `config.py`**
```python
# backend/config.py
LLM_MODEL: str = "llama-3.1-8b-instant"
LLM_TEMPERATURE: float = 0.0
```

**Option 3: Edit `agent.py` directly**
```python
# backend/agent.py (around line 30)
self.llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Change model here
    temperature=0
)
```

### Restart Server
After changing the model, restart the backend:
```bash
# Stop with Ctrl+C
python main.py
```

---

## 📁 Project Structure

```
pmmpl-production-ai-ChatBot/
│
├── backend/                    # FastAPI Backend
│   ├── main.py                 # FastAPI app entry point
│   ├── agent.py                # LangGraph AI agent (core logic)
│   ├── config.py               # Environment configuration
│   ├── database.py             # SQLAlchemy models
│   ├── models.py               # Pydantic request/response models
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (DO NOT COMMIT)
│   ├── .env.example            # Example environment file
│   └── credentials.json        # Google credentials (DO NOT COMMIT)
│
├── frontend/                   # Web Interface
│   ├── index.html              # Main HTML file
│   ├── style.css               # Styling
│   └── app.js                  # JavaScript logic
│
├── Untitled50.ipynb            # Jupyter notebook (development)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "GOOGLE_SHEETS_CREDENTIALS_PATH not found"
```
Error: Could not find credentials file
```
**Solution:**
- Ensure `credentials.json` is in `backend/` folder
- Check `.env` has correct path: `GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json`

#### 2. "Permission denied" on Google Sheets
```
Error: 403 - The caller does not have permission
```
**Solution:**
- Share Google Sheet with service account email
- Check the email in `credentials.json` → `client_email`

#### 3. "GROQ_API_KEY invalid"
```
Error: Invalid API key
```
**Solution:**
- Get new key from https://console.groq.com
- Update `.env`: `GROQ_API_KEY=gsk_your_new_key`

#### 4. "Module not found"
```
ModuleNotFoundError: No module named 'langchain_groq'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 5. "CORS error" in browser
```
Access-Control-Allow-Origin error
```
**Solution:**
- Add your frontend URL to `.env`:
  ```env
  CORS_ORIGINS=["http://localhost:5500", "http://127.0.0.1:5500"]
  ```

#### 6. "Database locked"
```
sqlite3.OperationalError: database is locked
```
**Solution:**
- Stop all Python processes
- Delete `chat_history.db`
- Restart server

### Debug Mode

Enable detailed logging:
```python
# backend/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔒 Security

### ⚠️ CRITICAL: Never Commit Secrets!

These files should NEVER be committed to Git:
- `.env` (contains API keys)
- `credentials.json` (Google credentials)
- `*.json` credential files

### Verify .gitignore

Ensure `.gitignore` contains:
```gitignore
# Secrets
.env
*.json
credentials.json

# Database
*.db
*.sqlite
```

### Rotate Compromised Keys

If you accidentally commit secrets:
1. **Immediately revoke/regenerate** the exposed keys
2. Use `git filter-repo` to remove from history
3. Force push the cleaned repo

---

## 📝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Prabhat**
- GitHub: [@Prabhat9801](https://github.com/Prabhat9801)

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [Groq](https://groq.com/) - Fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [gspread](https://gspread.readthedocs.io/) - Google Sheets API wrapper

---

<p align="center">
  Made with ❤️ for PMMPL Production Management
</p>

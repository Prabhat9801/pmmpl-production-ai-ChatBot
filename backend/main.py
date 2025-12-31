"""
FastAPI Backend for Google Sheets AI Agent.
Features:
- Chat interface with natural language queries
- SQLite-based chat history (Supabase-ready)
- Auto-refresh Google Sheets every 10 minutes
- CORS enabled for frontend communication
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime
from typing import List

from config import settings
from database import init_db, get_db, ChatHistory
from models import (
    ChatRequest, ChatResponse, ChatHistoryResponse, 
    ChatHistoryItem, HealthResponse
)
from agent import get_agent, GoogleSheetsAgent

# Background task for auto-refresh
async def auto_refresh_sheets():
    """Background task to refresh Google Sheets data every 10 minutes."""
    while True:
        await asyncio.sleep(settings.SHEETS_REFRESH_INTERVAL_MINUTES * 60)
        try:
            agent = get_agent()
            agent.refresh_data()
            print(f"✅ Auto-refresh completed at {datetime.utcnow()}")
        except Exception as e:
            print(f"❌ Auto-refresh failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting FastAPI backend...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Initialize agent (loads Google Sheets)
    get_agent()
    print("✅ Agent initialized")
    
    # Start background refresh task
    refresh_task = asyncio.create_task(auto_refresh_sheets())
    print(f"✅ Auto-refresh scheduled every {settings.SHEETS_REFRESH_INTERVAL_MINUTES} minutes")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down FastAPI backend...")
    refresh_task.cancel()


# Create FastAPI app
app = FastAPI(
    title="Google Sheets AI Agent API",
    description="Natural language interface for querying Google Sheets data",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API info."""
    return {
        "message": "Google Sheets AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.delete("/sessions/{session_id}/cache", tags=["Sessions"])
async def clear_session_cache(session_id: str):
    """
    Clear cache for a specific session.
    Called when user deletes a session or clears conversation history.
    """
    try:
        agent = get_agent()
        result = agent.clear_session_cache(session_id)
        return {
            "status": "success",
            "message": f"Cleared cache for session {session_id}",
            "deleted_count": result.get("deleted", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint - shows system status."""
    agent = get_agent()
    stats = agent.get_stats()
    
    return HealthResponse(
        status="healthy" if stats["sheets_loaded"] else "degraded",
        sheets_loaded=stats["sheets_loaded"],
        last_refresh=stats["last_refresh"],
        total_rows=stats["total_rows"]
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint - processes natural language questions.
    
    - Queries Google Sheets data using AI agent
    - Stores conversation in chat history
    - Returns answer with optional data preview
    - Supports conversation context (last 20 messages)
    """
    try:
        # Get agent and process question with conversation context
        agent = get_agent()
        
        # Check if it's a greeting or casual message (not a data query)
        greeting_keywords = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'thanks', 'thank you', 'bye', 'goodbye']
        question_lower = request.question.lower().strip()
        
        if question_lower in greeting_keywords or len(request.question.strip()) < 3:
            # Handle greetings without querying data
            greeting_responses = {
                'hi': "Hello! How can I help you with your data today?",
                'hello': "Hi there! What would you like to know about your data?",
                'hey': "Hey! I'm ready to help you analyze your data.",
                'thanks': "You're welcome! Let me know if you need anything else.",
                'thank you': "You're welcome! Feel free to ask more questions.",
                'bye': "Goodbye! Come back anytime you need data insights.",
                'goodbye': "Goodbye! Happy to help anytime."
            }
            
            return ChatResponse(
                answer=greeting_responses.get(question_lower, "Hello! How can I assist you with your data?"),
                confidence=1.0,
                rows_found=0,
                data_preview=None,
                query_type="GREETING",
                error=None
            )
        
        # Build context string from conversation history
        context = ""
        if request.conversation_history:
            context_lines = []
            for msg in request.conversation_history:
                if msg.role == 'system':
                    context_lines.append(f"Context: {msg.content}")
                elif msg.role == 'user':
                    context_lines.append(f"User: {msg.content}")
                elif msg.role == 'assistant':
                    context_lines.append(f"Assistant: {msg.content}")
            context = "\n".join(context_lines)
        
        # Add context to the question if available
        full_question = request.question
        if context:
            full_question = f"Conversation context:\n{context}\n\nCurrent question: {request.question}"
        
        result = agent.query(full_question, session_id=request.session_id)
        
        # Clean NaN/infinity values for JSON serialization
        import math
        def clean_value(val):
            if isinstance(val, float):
                if math.isnan(val) or math.isinf(val):
                    return None
            return val
        
        # Clean data preview if present
        if result.get("data_preview"):
            result["data_preview"] = [
                {k: clean_value(v) for k, v in row.items()}
                for row in result["data_preview"]
            ]
        
        # Clean numeric fields
        confidence = result.get("confidence")
        if isinstance(confidence, float) and (math.isnan(confidence) or math.isinf(confidence)):
            confidence = 0.5
        
        # Save to database
        chat_record = ChatHistory(
            session_id=request.session_id,
            user_question=request.question,
            bot_response=result["answer"],
            confidence=confidence,
            rows_found=result.get("rows_found"),
            query_type=result.get("query_type"),
            timestamp=datetime.utcnow()
        )
        db.add(chat_record)
        db.commit()
        
        # Return response
        return ChatResponse(
            answer=result["answer"],
            confidence=confidence,
            rows_found=result.get("rows_found"),
            data_preview=result.get("data_preview"),
            query_type=result.get("query_type"),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/history", response_model=ChatHistoryResponse, tags=["History"])
async def get_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get chat history.
    
    - Returns recent chat conversations
    - Supports pagination with limit and offset
    """
    try:
        # Get total count
        total = db.query(ChatHistory).count()
        
        # Get history with pagination
        history = db.query(ChatHistory)\
            .order_by(ChatHistory.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return ChatHistoryResponse(
            history=[ChatHistoryItem.model_validate(item) for item in history],
            total=total
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.delete("/history/{chat_id}", tags=["History"])
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """Delete a specific chat from history."""
    try:
        chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        db.delete(chat)
        db.commit()
        
        return {"message": "Chat deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")


@app.delete("/history", tags=["History"])
async def clear_history(db: Session = Depends(get_db)):
    """Clear all chat history."""
    try:
        db.query(ChatHistory).delete()
        db.commit()
        return {"message": "All chat history cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")


@app.post("/refresh", tags=["Admin"])
async def manual_refresh():
    """Manually trigger a refresh of Google Sheets data."""
    try:
        agent = get_agent()
        agent.refresh_data()
        return {
            "message": "Data refreshed successfully",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )

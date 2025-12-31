"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class ConversationMessage(BaseModel):
    """A single message in the conversation history."""
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(..., min_length=1, description="User's question")
    session_id: Optional[str] = Field(None, description="Optional session ID for tracking")
    conversation_history: Optional[List[ConversationMessage]] = Field(
        None, 
        description="Previous conversation context (last 20 messages + summary)"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="Bot's answer")
    confidence: Optional[float] = Field(None, description="Confidence score (0-1)")
    rows_found: Optional[int] = Field(None, description="Number of rows found")
    data_preview: Optional[List[dict]] = Field(None, description="Preview of data if applicable")
    query_type: Optional[str] = Field(None, description="Type of query executed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistoryItem(BaseModel):
    """Model for chat history item."""
    id: int
    user_question: str
    bot_response: str
    confidence: Optional[float]
    rows_found: Optional[int]
    query_type: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    history: List[ChatHistoryItem]
    total: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    sheets_loaded: bool
    last_refresh: Optional[datetime]
    total_rows: Optional[int]

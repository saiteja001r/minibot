from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import Base, engine, SessionLocal
from models import ChatMessage
from schemas import ChatMessageCreate, ChatMessageResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Chatbot Backend")

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CONFIG ---
MAX_MESSAGES_PER_HOUR = 5  # change as needed


@app.post("/chat", response_model=ChatMessageResponse)
def send_message(data: ChatMessageCreate, db: Session = Depends(get_db)):
    """
    Save a message if user hasn't exceeded message limit per hour.
    """

    # Get current and 1-hour-old timestamps
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    # Count user messages in last hour
    recent_msgs = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == data.user_id)
        .filter(ChatMessage.timestamp >= one_hour_ago)
        .count()
    )

    if recent_msgs >= MAX_MESSAGES_PER_HOUR:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit reached. You can send a new message after 1 hour.",
        )

    # Save the message
    new_msg = ChatMessage(user_id=data.user_id, message=data.message)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg


@app.get("/chat/{user_id}", response_model=list[ChatMessageResponse])
def get_messages(user_id: str, db: Session = Depends(get_db)):
    """Fetch all chat messages by user."""
    msgs = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).all()
    return msgs


@app.get("/")
def root():
    return {"message": "Chatbot backend is running!"}

"""
MongoDB async database layer for trading sessions.
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase, AsyncCollection
import pymongo
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import os


# ============================================================================
# Pydantic Models (Schemas)
# ============================================================================

class TradeStep(BaseModel):
    """Schema for individual trade steps during training."""
    timestamp: float
    price: float
    action: int  # 0: Sell, 1: Hold, 2: Buy
    reward: float
    agent_confidence: float
    observation: List[float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": 100.0,
                "price": 150.25,
                "action": 2,
                "reward": 0.05,
                "agent_confidence": 0.85,
                "observation": [0.1, 0.2, 0.3]
            }
        }


class TradingSession(BaseModel):
    """Schema for a complete trading session."""
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    initial_balance: float
    final_balance: float
    total_return: float = 0.0  # (final - initial) / initial
    episode_reward: float = 0.0  # Total reward from training
    num_steps: int = 0
    status: str = "queued"  # queued, training, completed, failed
    steps: List[TradeStep] = []
    model_version: str = "PPO-v1.0"
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2024-01-15T10:30:00",
                "completed_at": "2024-01-15T10:45:00",
                "initial_balance": 10000.0,
                "final_balance": 10500.0,
                "total_return": 0.05,
                "episode_reward": 100.5,
                "num_steps": 500,
                "status": "completed",
                "steps": [],
                "model_version": "PPO-v1.0"
            }
        }


# ============================================================================
# MongoDB Client
# ============================================================================

class MongoDBClient:
    """Async MongoDB client for trading sessions."""
    
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "trading_agent"):
        """
        Initialize MongoDB client.
        
        Args:
            uri: MongoDB connection URI
            db_name: Database name
        """
        self.uri = uri
        self.db_name = db_name
        self.client: Optional[AsyncClient] = None
        self.db: Optional[AsyncDatabase] = None
    
    async def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            self.client = AsyncClient(self.uri)
            self.db = self.client[self.db_name]
            
            # Create indexes
            collection = self.db["trading_sessions"]
            await collection.create_index("session_id", unique=True)
            await collection.create_index("created_at")
            await collection.create_index("status")
            
            # Test connection
            await self.client.admin.command("ping")
            print(f"✓ Connected to MongoDB: {self.db_name}")
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            print("✓ Disconnected from MongoDB")
    
    async def create_session(self, session: TradingSession) -> str:
        """
        Create a new trading session.
        
        Args:
            session: TradingSession object
            
        Returns:
            Session ID
        """
        collection = self.db["trading_sessions"]
        doc = {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "completed_at": session.completed_at,
            "initial_balance": session.initial_balance,
            "final_balance": session.final_balance,
            "total_return": session.total_return,
            "episode_reward": session.episode_reward,
            "num_steps": session.num_steps,
            "status": session.status,
            "steps": [step.dict() for step in session.steps],
            "model_version": session.model_version,
        }
        
        try:
            result = await collection.insert_one(doc)
            return str(result.inserted_id)
        except DuplicateKeyError:
            raise ValueError(f"Session {session.session_id} already exists")
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a trading session by ID.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            Session document or None if not found
        """
        collection = self.db["trading_sessions"]
        return await collection.find_one({"session_id": session_id})
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a trading session.
        
        Args:
            session_id: Session ID to update
            updates: Dictionary of fields to update
            
        Returns:
            True if updated, False if not found
        """
        collection = self.db["trading_sessions"]
        result = await collection.update_one(
            {"session_id": session_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def add_step(self, session_id: str, step: TradeStep) -> bool:
        """
        Add a step to a trading session.
        
        Args:
            session_id: Session ID
            step: TradeStep object
            
        Returns:
            True if successful
        """
        collection = self.db["trading_sessions"]
        result = await collection.update_one(
            {"session_id": session_id},
            {"$push": {"steps": step.dict()}}
        )
        return result.modified_count > 0
    
    async def get_all_sessions(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get all trading sessions with optional filtering.
        
        Args:
            status: Filter by status (optional)
            limit: Maximum number of sessions to return
            skip: Number of sessions to skip
            
        Returns:
            List of session documents
        """
        collection = self.db["trading_sessions"]
        query = {}
        
        if status:
            query["status"] = status
        
        cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        return await cursor.to_list(length=limit)
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a trading session.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        collection = self.db["trading_sessions"]
        result = await collection.delete_one({"session_id": session_id})
        return result.deleted_count > 0


# ============================================================================
# Singleton Instance
# ============================================================================

_db_client: Optional[MongoDBClient] = None


async def get_db_client() -> MongoDBClient:
    """
    Get or create MongoDB client (singleton pattern).
    
    Returns:
        MongoDBClient instance
    """
    global _db_client
    
    if _db_client is None:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        _db_client = MongoDBClient(uri=uri, db_name="trading_agent")
        await _db_client.connect()
    
    return _db_client

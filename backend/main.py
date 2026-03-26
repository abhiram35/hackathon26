"""
FastAPI backend for RL Trading Agent.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import numpy as np
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import asyncio
from pydantic import BaseModel

# RL and ML imports
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import StopTrainingOnRewardThreshold
import gymnasium as gym

# Local imports
from database import MongoDBClient, TradingSession, TradeStep, get_db_client
from environment import TradingEnv


# ============================================================================
# Pydantic Request/Response Models
# ============================================================================

class TrainRequest(BaseModel):
    """Request body for training endpoint."""
    episodes: int = 100
    total_timesteps: int = 10000
    price_data: List[float]
    initial_balance: float = 10000.0
    session_name: Optional[str] = None


class TrainResponse(BaseModel):
    """Response for training endpoint."""
    session_id: str
    status: str
    message: str


class ReplayResponse(BaseModel):
    """Response for replay endpoint."""
    session_id: str
    created_at: str
    completed_at: Optional[str]
    initial_balance: float
    final_balance: float
    total_return: float
    num_steps: int
    status: str
    steps: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    database: str
    timestamp: str


# ============================================================================
# Global State
# ============================================================================

db_client: Optional[MongoDBClient] = None
active_sessions: Dict[str, asyncio.Task] = {}


# ============================================================================
# Lifecycle Management
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage FastAPI application lifecycle.
    Startup: Connect to MongoDB
    Shutdown: Cleanup resources
    """
    global db_client
    print("🚀 Starting Trading Agent API...")
    
    # Startup
    db_client = await get_db_client()
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Trading Agent API...")
    if db_client:
        await db_client.disconnect()


# ============================================================================
# FastAPI App Initialization
# ============================================================================

app = FastAPI(
    title="RL Trading Agent API",
    description="Backend for Reinforcement Learning trading agent",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Dependency Injection
# ============================================================================

async def get_db() -> MongoDBClient:
    """Dependency: Get database client."""
    if db_client is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db_client


# ============================================================================
# Training Logic
# ============================================================================

async def train_agent_background(
    session_id: str,
    price_data: np.ndarray,
    initial_balance: float,
    total_timesteps: int,
    db: MongoDBClient,
) -> None:
    """
    Background task for PPO training.
    
    Args:
        session_id: Unique training session ID
        price_data: Historical price data
        initial_balance: Starting capital
        total_timesteps: Total training timesteps
        db: Database client
    """
    try:
        print(f"\n📊 Starting training for session {session_id}")
        print(f"   Timesteps: {total_timesteps}, Balance: ${initial_balance}")
        
        # Update session status
        await db.update_session(session_id, {
            "status": "training",
            "started_at": datetime.utcnow()
        })
        
        # Create environment
        env = TradingEnv(
            price_data=price_data,
            initial_balance=initial_balance,
            window_size=20,
            transaction_cost=0.001,
        )
        
        # Wrap in DummyVecEnv for stable-baselines3 compatibility
        vec_env = DummyVecEnv([lambda: env])
        
        # Create PPO agent
        model = PPO(
            "MlpPolicy",
            vec_env,
            learning_rate=3e-4,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
            verbose=1,
        )
        
        # Custom callback for tracking
        class TrainingCallback:
            def __init__(self, db: MongoDBClient, session_id: str):
                self.db = db
                self.session_id = session_id
                self.best_reward = float('-inf')
            
            async def on_step(self, step: int, reward: float) -> None:
                """Called after each step."""
                if reward > self.best_reward:
                    self.best_reward = reward
                    await self.db.update_session(
                        self.session_id,
                        {"best_reward": self.best_reward}
                    )
        
        callback = TrainingCallback(db, session_id)
        
        # Train the model
        model.learn(
            total_timesteps=total_timesteps,
            progress_bar=True,
        )
        
        print(f"✅ Training completed for session {session_id}")
        
        # Run final evaluation
        observation, info = env.reset()
        episode_reward = 0.0
        all_steps: List[TradeStep] = []
        
        for step in range(len(price_data) - 21):
            action, _states = model.predict(observation, deterministic=True)
            observation, reward, terminated, truncated, step_info = env.step(action)
            episode_reward += reward
            
            # Record step with confidence
            trade_step = TradeStep(
                timestamp=float(step),
                price=step_info["price"],
                action=int(action),
                reward=step_info["reward"],
                agent_confidence=step_info["agent_confidence"],
                observation=env._get_observation().tolist()
            )
            all_steps.append(trade_step)
            
            if terminated or truncated:
                break
        
        final_portfolio_value = env.get_portfolio_value()
        total_return = (final_portfolio_value - initial_balance) / initial_balance
        
        # Save session to database
        await db.update_session(session_id, {
            "status": "completed",
            "completed_at": datetime.utcnow(),
            "episode_reward": episode_reward,
            "total_return": total_return,
            "final_balance": final_portfolio_value,
            "num_steps": len(all_steps),
            "steps": [step.dict() for step in all_steps],
        })
        
        # Save model
        model_path = f"/tmp/model_{session_id}"
        model.save(model_path)
        print(f"💾 Model saved to {model_path}")
        
        # Cleanup
        vec_env.close()
        
    except Exception as e:
        print(f"❌ Training failed for session {session_id}: {str(e)}")
        await db.update_session(session_id, {
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.utcnow()
        })


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: MongoDBClient = Depends(get_db)) -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        Health status and database connectivity
    """
    try:
        # Test database connection
        await db.get_all_sessions(limit=1)
        db_status = "✓ Connected"
    except Exception as e:
        db_status = f"✗ Error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/train", response_model=TrainResponse, tags=["Training"])
async def train(
    request: TrainRequest,
    background_tasks: BackgroundTasks,
    db: MongoDBClient = Depends(get_db),
) -> TrainResponse:
    """
    Trigger a training session.
    
    The training runs as a background task. Use GET /replay/{session_id} to fetch results.
    
    Args:
        request: Training configuration
        background_tasks: FastAPI background tasks
        db: Database client
        
    Returns:
        Response with session ID and status
    """
    # Validate input
    if not request.price_data or len(request.price_data) < 50:
        raise HTTPException(status_code=400, detail="Price data must have at least 50 points")
    
    if request.total_timesteps < 1000:
        raise HTTPException(status_code=400, detail="total_timesteps must be >= 1000")
    
    # Create session
    session_id = str(uuid.uuid4())
    session = TradingSession(
        session_id=session_id,
        initial_balance=request.initial_balance,
        final_balance=request.initial_balance,
        model_version="PPO-v1.0",
        status="queued",
    )
    
    await db.create_session(session)
    
    # Queue background training task
    price_data = np.array(request.price_data, dtype=np.float32)
    background_tasks.add_task(
        train_agent_background,
        session_id,
        price_data,
        request.initial_balance,
        request.total_timesteps,
        db
    )
    
    return TrainResponse(
        session_id=session_id,
        status="queued",
        message=f"Training session {session_id} queued. Check status with GET /replay/{session_id}"
    )


@app.get("/replay/{session_id}", response_model=ReplayResponse, tags=["Replay"])
async def get_replay(
    session_id: str,
    db: MongoDBClient = Depends(get_db),
) -> ReplayResponse:
    """
    Fetch a completed trading session.
    
    Args:
        session_id: ID of the session to retrieve
        db: Database client
        
    Returns:
        Complete trading session with all steps and metrics
        
    Raises:
        HTTPException: If session not found
    """
    session_doc = await db.get_session(session_id)
    
    if not session_doc:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return ReplayResponse(
        session_id=session_doc["session_id"],
        created_at=session_doc["created_at"].isoformat(),
        completed_at=session_doc.get("completed_at", "").isoformat() if session_doc.get("completed_at") else None,
        initial_balance=session_doc["initial_balance"],
        final_balance=session_doc["final_balance"],
        total_return=session_doc["total_return"],
        num_steps=session_doc["num_steps"],
        status=session_doc["status"],
        steps=session_doc.get("steps", []),
    )


@app.get("/sessions", tags=["Sessions"])
async def list_sessions(
    status: Optional[str] = None,
    limit: int = 50,
    db: MongoDBClient = Depends(get_db),
) -> Dict[str, Any]:
    """
    List all training sessions.
    
    Args:
        status: Filter by status (optional)
        limit: Maximum number of sessions
        db: Database client
        
    Returns:
        List of sessions with summary statistics
    """
    sessions = await db.get_all_sessions(status=status, limit=limit)
    
    # Compute statistics
    total_sessions = len(sessions)
    completed_sessions = sum(1 for s in sessions if s["status"] == "completed")
    avg_return = np.mean([s.get("total_return", 0) for s in sessions if s["status"] == "completed"]) if completed_sessions > 0 else 0
    
    return {
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "avg_return": float(avg_return),
        "sessions": [
            {
                "session_id": s["session_id"],
                "status": s["status"],
                "created_at": s["created_at"].isoformat(),
                "completed_at": s.get("completed_at", "").isoformat() if s.get("completed_at") else None,
                "total_return": s.get("total_return", 0),
                "num_steps": s.get("num_steps", 0),
            }
            for s in sessions
        ]
    }


@app.get("/sessions/{session_id}/stats", tags=["Sessions"])
async def get_session_stats(
    session_id: str,
    db: MongoDBClient = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get detailed statistics for a session.
    
    Args:
        session_id: ID of the session
        db: Database client
        
    Returns:
        Detailed performance metrics and analytics
        
    Raises:
        HTTPException: If session not found
    """
    session_doc = await db.get_session(session_id)
    
    if not session_doc:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    steps = session_doc.get("steps", [])
    
    # Calculate metrics
    if steps:
        confidences = [s["agent_confidence"] for s in steps]
        rewards = [s["reward"] for s in steps]
        actions = [s["action"] for s in steps]
        
        buy_count = sum(1 for a in actions if a == 2)
        sell_count = sum(1 for a in actions if a == 0)
        hold_count = sum(1 for a in actions if a == 1)
        
        avg_confidence = float(np.mean(confidences)) if confidences else 0.0
        max_confidence = float(np.max(confidences)) if confidences else 0.0
        min_confidence = float(np.min(confidences)) if confidences else 0.0
    else:
        avg_confidence = 0.0
        max_confidence = 0.0
        min_confidence = 0.0
        buy_count = 0
        sell_count = 0
        hold_count = 0
    
    return {
        "session_id": session_id,
        "status": session_doc["status"],
        "initial_balance": session_doc["initial_balance"],
        "final_balance": session_doc["final_balance"],
        "total_return": f"{session_doc.get('total_return', 0) * 100:.2f}%",
        "num_steps": session_doc["num_steps"],
        "agent_confidence": {
            "average": avg_confidence,
            "max": max_confidence,
            "min": min_confidence,
        },
        "actions": {
            "buy": buy_count,
            "sell": sell_count,
            "hold": hold_count,
        },
        "duration_minutes": (
            (session_doc.get("completed_at") - session_doc["created_at"]).total_seconds() / 60
            if session_doc.get("completed_at")
            else None
        ),
    }


@app.delete("/sessions/{session_id}", tags=["Sessions"])
async def delete_session(
    session_id: str,
    db: MongoDBClient = Depends(get_db),
) -> Dict[str, str]:
    """
    Delete a training session.
    
    Args:
        session_id: ID of the session to delete
        db: Database client
        
    Returns:
        Confirmation message
        
    Raises:
        HTTPException: If session not found
    """
    success = await db.delete_session(session_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return {"message": f"Session {session_id} deleted successfully"}


# ============================================================================
# Utility Endpoints
# ============================================================================

@app.get("/", tags=["Info"])
async def root() -> Dict[str, str]:
    """API information endpoint."""
    return {
        "name": "RL Trading Agent API",
        "version": "1.0.0",
        "description": "Backend for Reinforcement Learning trading agent with PPO",
        "docs": "/docs",
    }


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

"""
Configuration and settings for the RL Trading Agent.
Customize these values based on your requirements.
"""

import os
from typing import Optional

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# MongoDB connection URI
# Local: mongodb://localhost:27017
# Atlas: mongodb+srv://user:password@cluster.mongodb.net/database
MONGODB_URI: str = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)

# Database name
DB_NAME: str = "trading_agent"

# Collection names
SESSIONS_COLLECTION: str = "trading_sessions"


# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

class EnvironmentConfig:
    """Configuration for TradingEnv"""
    
    # Window size for price history in observation space
    WINDOW_SIZE: int = 20
    
    # Starting capital in USD
    INITIAL_BALANCE: float = 10000.0
    
    # Transaction cost as percentage (0.1% = 0.001)
    TRANSACTION_COST: float = 0.001
    
    # Technical indicator periods
    RSI_PERIOD: int = 14
    MACD_FAST: int = 12
    MACD_SLOW: int = 26
    MACD_SIGNAL: int = 9
    VOLUME_PERIOD: int = 20
    
    # Reward configuration
    REWARD_SCALE: float = 100.0  # Scale log returns
    UNDERWATER_PENALTY: float = 0.5  # Penalty for losing trades
    TRADE_PENALTY: float = 0.1  # Penalty for each trade
    
    # Maximum episode steps (None = len(price_data) - window_size - 1)
    MAX_STEPS: Optional[int] = None


# ============================================================================
# RL MODEL CONFIGURATION
# ============================================================================

class RLModelConfig:
    """Configuration for PPO model training"""
    
    # Policy network type
    POLICY_TYPE: str = "MlpPolicy"
    
    # Learning rate
    LEARNING_RATE: float = 3e-4
    
    # Number of steps to collect before updating policy
    N_STEPS: int = 2048
    
    # Batch size for training
    BATCH_SIZE: int = 64
    
    # Number of epochs for each update
    N_EPOCHS: int = 10
    
    # Discount factor (gamma)
    GAMMA: float = 0.99
    
    # GAE lambda (for advantage estimation)
    GAE_LAMBDA: float = 0.95
    
    # Clipping range for PPO loss
    CLIP_RANGE: float = 0.2
    
    # Entropy coefficient (for exploration)
    ENT_COEF: float = 0.0
    
    # Value function coefficient
    VF_COEF: float = 0.5
    
    # Maximum gradient norm (prevent exploding gradients)
    MAX_GRAD_NORM: float = 0.5
    
    # Device: 'auto', 'cpu', or 'cuda'
    DEVICE: str = "auto"
    
    # Verbose output level (0: no output, 1: progress, 2: detailed)
    VERBOSE: int = 1


# ============================================================================
# TRAINING CONFIGURATION
# ============================================================================

class TrainingConfig:
    """Configuration for training sessions"""
    
    # Default total timesteps for training
    DEFAULT_TOTAL_TIMESTEPS: int = 10000
    
    # Default number of episodes
    DEFAULT_EPISODES: int = 100
    
    # Reward threshold for early stopping (optional)
    REWARD_THRESHOLD: Optional[float] = None
    
    # Save model every N steps
    SAVE_INTERVAL: int = 10000
    
    # Model storage path (relative to project root)
    MODEL_PATH: str = "./models"
    
    # Log path for tensorboard
    LOG_PATH: str = "./logs"


# ============================================================================
# API CONFIGURATION
# ============================================================================

class APIConfig:
    """Configuration for FastAPI server"""
    
    # Server host
    HOST: str = "0.0.0.0"
    
    # Server port
    PORT: int = 8000
    
    # Enable CORS (for frontend access)
    ENABLE_CORS: bool = True
    
    # CORS origins (default: all origins)
    CORS_ORIGINS: list = ["*"]
    
    # Request timeout (seconds)
    REQUEST_TIMEOUT: int = 300
    
    # Max sessions to return in list endpoints
    MAX_SESSIONS_LIMIT: int = 100
    
    # Default sessions limit
    DEFAULT_SESSIONS_LIMIT: int = 50


# ============================================================================
# CONFIDENCE/SALIENCY SCORING
# ============================================================================

class ConfidenceConfig:
    """Configuration for agent confidence scoring"""
    
    # RSI thresholds for bullish/bearish classification
    RSI_BULLISH_THRESHOLD: float = 0.7
    RSI_BEARISH_THRESHOLD: float = 0.3
    
    # MACD thresholds
    MACD_BULLISH_THRESHOLD: float = 0.6
    MACD_BEARISH_THRESHOLD: float = 0.4
    
    # Neutral confidence (for Hold action)
    NEUTRAL_CONFIDENCE: float = 0.5
    
    # Confidence calculation method: 'indicator_alignment' or 'model_entropy'
    METHOD: str = "indicator_alignment"


# ============================================================================
# LOGGING & MONITORING
# ============================================================================

class LoggingConfig:
    """Configuration for logging and monitoring"""
    
    # Log level: DEBUG, INFO, WARNING, ERROR
    LOG_LEVEL: str = "INFO"
    
    # Log file path
    LOG_FILE: str = "./logs/trading_agent.log"
    
    # Enable request logging
    LOG_REQUESTS: bool = True
    
    # Enable database query logging
    LOG_DB_QUERIES: bool = False
    
    # Save metrics every N steps
    METRICS_INTERVAL: int = 100


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_environment_config() -> EnvironmentConfig:
    """Get environment configuration."""
    return EnvironmentConfig()


def get_rl_model_config() -> RLModelConfig:
    """Get RL model configuration."""
    return RLModelConfig()


def get_training_config() -> TrainingConfig:
    """Get training configuration."""
    return TrainingConfig()


def get_api_config() -> APIConfig:
    """Get API configuration."""
    return APIConfig()


def get_confidence_config() -> ConfidenceConfig:
    """Get confidence scoring configuration."""
    return ConfidenceConfig()


def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return LoggingConfig()


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

class PresetConfigs:
    """Preset configuration bundles for different scenarios"""
    
    @staticmethod
    def quick_test() -> dict:
        """Fast training for testing - ~2 minutes"""
        return {
            "total_timesteps": 2000,
            "episodes": 10,
            "window_size": 10,
            "batch_size": 32,
        }
    
    @staticmethod
    def standard() -> dict:
        """Standard training - ~10 minutes"""
        return {
            "total_timesteps": 10000,
            "episodes": 50,
            "window_size": 20,
            "batch_size": 64,
        }
    
    @staticmethod
    def intensive() -> dict:
        """Intensive training - ~30+ minutes"""
        return {
            "total_timesteps": 50000,
            "episodes": 200,
            "window_size": 30,
            "batch_size": 128,
        }
    
    @staticmethod
    def production() -> dict:
        """Production-grade training"""
        return {
            "total_timesteps": 100000,
            "episodes": 500,
            "window_size": 40,
            "batch_size": 256,
            "learning_rate": 1e-4,
            "n_epochs": 20,
        }


# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> bool:
    """Validate configuration values."""
    errors = []
    
    # Environment config validation
    if EnvironmentConfig.WINDOW_SIZE < 5:
        errors.append("WINDOW_SIZE must be >= 5")
    
    if EnvironmentConfig.INITIAL_BALANCE <= 0:
        errors.append("INITIAL_BALANCE must be > 0")
    
    if not (0 <= EnvironmentConfig.TRANSACTION_COST < 0.1):
        errors.append("TRANSACTION_COST must be between 0 and 0.1")
    
    # RL Model config validation
    if RLModelConfig.LEARNING_RATE <= 0:
        errors.append("LEARNING_RATE must be > 0")
    
    if RLModelConfig.GAMMA < 0 or RLModelConfig.GAMMA > 1:
        errors.append("GAMMA must be between 0 and 1")
    
    # API config validation
    if APIConfig.PORT < 1024 or APIConfig.PORT > 65535:
        errors.append("PORT must be between 1024 and 65535")
    
    if errors:
        print("⚠️  Configuration validation errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    return True


if __name__ == "__main__":
    print("="*70)
    print("RL Trading Agent - Configuration")
    print("="*70)
    
    print("\n📁 Database:")
    print(f"   URI: {MONGODB_URI}")
    print(f"   Database: {DB_NAME}")
    
    print("\n🎮 Environment:")
    env_cfg = get_environment_config()
    print(f"   Window Size: {env_cfg.WINDOW_SIZE}")
    print(f"   Initial Balance: ${env_cfg.INITIAL_BALANCE:,.2f}")
    print(f"   Transaction Cost: {env_cfg.TRANSACTION_COST*100:.2f}%")
    
    print("\n🤖 RL Model:")
    rl_cfg = get_rl_model_config()
    print(f"   Learning Rate: {rl_cfg.LEARNING_RATE}")
    print(f"   Batch Size: {rl_cfg.BATCH_SIZE}")
    print(f"   Gamma: {rl_cfg.GAMMA}")
    
    print("\n📊 Training:")
    train_cfg = get_training_config()
    print(f"   Default Timesteps: {train_cfg.DEFAULT_TOTAL_TIMESTEPS:,}")
    print(f"   Model Path: {train_cfg.MODEL_PATH}")
    
    print("\n🔌 API:")
    api_cfg = get_api_config()
    print(f"   Host: {api_cfg.HOST}")
    print(f"   Port: {api_cfg.PORT}")
    
    print("\n✅ Validation:", "PASSED" if validate_config() else "FAILED")
    print()

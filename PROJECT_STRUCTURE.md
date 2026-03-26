# RL Trading Agent - Complete Project Structure

```
Hackathon/
│
├── 📦 BACKEND (FastAPI + MongoDB + Gymnasium)
│   └── backend/
│       ├── main.py                 # FastAPI server with 7 REST endpoints
│       ├── database.py             # MongoDB async client & schemas
│       ├── environment.py          # Custom Gymnasium trading env
│       ├── config.py               # Centralized configuration
│       └── requirements.txt        # Python dependencies
│
├── 🎨 FRONTEND (React Dashboard)
│   └── frontend/
│       ├── src/
│       │   ├── components/         # React components
│       │   │   ├── Dashboard.js
│       │   │   ├── TrainingControl.js
│       │   │   └── SessionList.js
│       │   ├── App.js              # Main app component
│       │   ├── App.css             # Styling
│       │   └── index.js            # React entry point
│       ├── public/
│       │   └── index.html          # HTML template
│       ├── package.json            # Node dependencies
│       └── README.md               # Frontend setup guide
│
├── 🤖 TRAINING (Standalone Scripts)
│   └── training/
│       ├── scripts/
│       │   ├── train.py            # Main training script
│       │   ├── evaluate.py         # Model evaluation & plots
│       │   └── data_utils.py       # Data generation/loading
│       ├── data/                   # Price data directory
│       ├── models/                 # Trained models storage
│       ├── requirements.txt        # Python dependencies
│       └── README.md               # Training guide
│
├── 📚 DOCUMENTATION
│   └── docs/
│       ├── README.md               # Main documentation
│       ├── FRAMEWORK.md            # Development roadmap (6 phases)
│       ├── ARCHITECTURE.md         # System design & components
│       ├── QUICKREF.md             # Command cheat sheet
│       ├── CHECKLIST.md            # Implementation checklist
│       ├── STATUS_DASHBOARD.md     # Project status overview
│       └── ERROR_CHECK_REPORT.md   # Validation results
│
├── 📋 EXAMPLES & TESTS
│   └── examples/
│       ├── example.py              # Quick-start walkthrough
│       ├── test_api.py             # API endpoint tests
│       ├── test_environment.py     # Environment validation
│       └── test_health.py          # Health check verification
│
├── 📝 LOGS & OUTPUTS
│   └── logs/                       # Training logs directory
│
├── ⚙️ ROOT CONFIG FILES
│   ├── .gitignore                  # Git ignore patterns
│   ├── PROJECT_STRUCTURE.md        # This file
│   └── .venv/                      # Python virtual environment
```

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py  # Starts FastAPI at http://localhost:8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start  # Starts React at http://localhost:3000
```

### 3. Training Setup
```bash
cd training
pip install -r requirements.txt
python scripts/data_utils.py  # Generate sample data
python scripts/train.py --data data/sample_prices.csv --evaluate  # Train model
```

---

## 📊 Component Overview

### Backend Services (✅ Complete)
- **FastAPI Server**: REST API with 7 endpoints
- **MongoDB**: Async database for session persistence
- **Trading Environment**: Gymnasium environment with technical indicators
- **Config System**: Centralized settings management

**Running at**: `http://localhost:8000`

### Frontend (🎨 Ready to Build)
- **Dashboard**: Real-time statistics and metrics
- **Training Control**: Start/monitor training sessions
- **Session Viewer**: View and replay past training runs

**Ready to run**: `npm start` in `/frontend`

### Training Tools (🤖 Ready to Use)
- **Standalone Training**: Run training independently
- **Model Evaluation**: Validate trained models
- **Data Utilities**: Generate or load price data

**Quick command**: `python scripts/train.py --help`

---

## 📦 Dependencies Overview

### Backend
- **fastapi** (API framework)
- **motor** (Async MongoDB)
- **gymnasium** (RL environment)
- **stable-baselines3** (PPO algorithm)
- **torch** (Deep learning)

### Frontend
- **react** (UI framework)
- **axios** (HTTP client)
- **chart.js** (Data visualization)

### Training
- **numpy**, **scipy** (Numerical computing)
- **pandas** (Data analysis)
- **matplotlib** (Plotting)

---

## 🔄 Development Phases

### ✅ Phase 0: Infrastructure (COMPLETED)
- Backend API setup & endpoints
- Database integration
- Trading environment creation
- Full test & validation

### 🔄 Phase 1: Local Validation (IN PROGRESS)
- Test with synthetic/sample data
- Validate training pipeline
- Document results

### ⏳ Phase 2: Frontend Dashboard (READY)
- React dashboard with charts
- Training control panel
- Session replay viewer

### ⏳ Phase 3: Live Market Data (PLANNED)
- Integration with market APIs
- Backtesting framework
- Real-time data streaming

### ⏳ Phase 4: Risk Metrics (PLANNED)
- Sharpe Ratio calculation
- Drawdown analysis
- Advanced analytics

### ⏳ Phase 5: Model Persistence (PLANNED)
- Model checkpointing
- Version management
- Model serving endpoints

---

## 🛠️ Common Commands

### Start Services
```bash
# Backend
cd backend && python main.py

# Frontend
cd frontend && npm start

# Training
cd training && python scripts/train.py --data data/sample_prices.csv
```

### Test & Validate
```bash
cd examples
python test_api.py
python test_environment.py
python test_health.py
```

### Monitor & Analyze
```bash
# View API docs
# http://localhost:8000/docs

# Check health
curl http://localhost:8000/health

# List sessions
curl http://localhost:8000/sessions
```

---

## 📂 File Organization Rules

1. **Backend code** → `/backend/`
2. **Frontend code** → `/frontend/src/` or `/frontend/public/`
3. **Training scripts** → `/training/scripts/`
4. **Documentation** → `/docs/`
5. **Tests & Examples** → `/examples/`
6. **Data files** → `/training/data/`
7. **Trained models** → `/training/models/`
8. **Logs & outputs** → `/logs/`
9. **Config files** → Root or respective module directories

---

## 🎯 Next Steps

1. **Frontend Dashboard** (Phase 2)
   - Build React components
   - Connect to backend API
   - Add charts and visualization

2. **Local Testing** (Phase 1)
   - Run training with sample data
   - Validate complete pipeline
   - Document results

3. **Live Integration** (Phase 3)
   - Add market data API
   - Create backtesting framework
   - Implement paper trading

See `/docs/FRAMEWORK.md` for detailed roadmap and task breakdown.

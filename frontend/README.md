# RL Trading Agent - Frontend Dashboard

Modern React dashboard with Tailwind CSS for monitoring and controlling the RL trading agent.

## 🎨 Tech Stack

- **React 18** - UI framework
- **Tailwind CSS 3** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **PostCSS + Autoprefixer** - CSS processing

## ⚡ Quick Start

### Installation
```bash
npm install
```

### Development Server
```bash
npm start
```
Opens http://localhost:3000 in your browser. Hot reload enabled.

### Production Build
```bash
npm build
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.js         # Statistics & metrics
│   │   ├── TrainingControl.js   # Training form & controls
│   │   └── SessionList.js       # Session history & management
│   ├── App.js                   # Main app component
│   ├── App.css                  # Tailwind imports & custom styles
│   └── index.js                 # React entry point
├── public/
│   └── index.html               # HTML template
├── package.json                 # Dependencies
├── tailwind.config.js           # Tailwind configuration
├── postcss.config.js            # PostCSS configuration
└── README.md                    # This file
```

## 🚀 Features

### Dashboard Component
- Total training sessions counter
- Completed sessions tracker
- Average return calculation
- Success rate percentage

### Training Control Panel
- Price data input (comma-separated values)
- Total timesteps configuration
- Initial balance customization
- Real-time training feedback
- Error handling & validation

### Session Management
- List all training sessions
- Expandable session details
- Delete completed sessions
- Status indicators (Completed, Training, Failed)
- Return performance display

## 🎨 Tailwind CSS Customization

Edit `tailwind.config.js` to customize:
```javascript
theme: {
  extend: {
    colors: {
      primary: '#667eea',
      secondary: '#764ba2',
    },
    animation: {
      'fade-in': 'fadeIn 0.3s ease-in-out',
    },
  },
}
```

## 📡 API Integration

Connects to backend at `http://localhost:8000`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend status |
| `/train` | POST | Start training session |
| `/sessions` | GET | List all sessions |
| `/sessions/{id}/stats` | GET | Get session statistics |
| `/sessions/{id}` | DELETE | Delete a session |

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from create-react-app (irreversible)

## 📦 Dependencies

### Production
- react@^18.2.0
- react-dom@^18.2.0
- axios@^1.6.0
- chart.js@^4.4.0
- react-chartjs-2@^5.2.0

### Development
- react-scripts@5.0.1
- tailwindcss@^3.4.1
- postcss@^8.4.33
- autoprefixer@^10.4.17
- @testing-library/react@^14.0.0

## 🎯 Usage Examples

### Access the Dashboard
```bash
npm start
# Then open http://localhost:3000
```

### Start Training from UI
1. Paste price data in textarea (comma-separated)
2. Adjust timesteps and balance if desired
3. Click "Start Training" button
4. Monitor progress in Sessions list

### View Training Results
- Check Dashboard for statistics
- Expand session card for details
- Click delete to remove old sessions

## 🔗 Connection with Backend

Make sure FastAPI backend is running:
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend will be available at http://localhost:8000  
API docs at http://localhost:8000/docs

## 🎓 Styling Guide

### Using Tailwind Classes
Component example with Tailwind:
```jsx
<button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 rounded-lg">
  Start Training
</button>
```

### Custom Animations
The `App.css` file includes custom animations:
- `fade-in` - Smooth fade in transition
- `pulse-custom` - Loading pulse effect

Apply with:
```jsx
<div className="fade-in">Content</div>
<div className="pulse-custom">Loading...</div>
```

## 🐛 Troubleshooting

### "Cannot find backend"
- Ensure FastAPI is running on `http://localhost:8000`
- Check CORS is enabled in backend

### Tailwind classes not applying
- Restart dev server: `npm start`
- Clear cache: `rm -rf node_modules && npm install`

### Form not submitting
- Check backend health: http://localhost:8000/health
- Open browser console for error details

## 📚 Resources

- [React Docs](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

## 🤝 Development Tips

1. **Component Organization**: Keep components in `/src/components/`
2. **Styling**: Use Tailwind utility classes, avoid CSS files
3. **State**: Use React hooks (useState, useEffect)
4. **API Calls**: Use axios or fetch API
5. **Testing**: Create test files alongside components

---

**Status**: ✅ Production Ready  
**Last Updated**: March 26, 2026  
**Tailwind CSS**: v3.4+

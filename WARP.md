
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **AI Green Habit Tracker**, a Flask-based web API that helps users track their environmental habits and provides AI-powered scoring and suggestions. The application uses NLP to categorize user habits, calculates environmental impact scores, and generates personalized recommendations for sustainable living.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.txt  # dev tools included in requirements.txt
```

### Running the Application
```bash
# Run the main application (development server)
python src/habit_tracker.py

# Run with custom configuration
FLASK_HOST=0.0.0.0 FLASK_PORT=8000 FLASK_DEBUG=true python src/habit_tracker.py

# Run using setuptools entry point (after installation)
pip install -e .
green-tracker
```

### Testing and Code Quality
```bash
# Run tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run single test file
python -m pytest tests/test_categorizer.py

# Code formatting
black src/

# Linting
flake8 src/
```

### API Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Log a habit
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d '{"habit": "took the bus to work instead of driving"}'

# Get green score
curl http://localhost:5000/api/score

# Get suggestions
curl http://localhost:5000/api/suggestions
```

## Architecture Overview

### Core Components Architecture

The application follows a modular Flask API design with four main components:

1. **habit_tracker.py** - Main Flask application and API endpoints
2. **nlp_categorizer.py** - Natural language processing for habit categorization
3. **scoring_system.py** - Environmental impact scoring calculations
4. **suggestions_engine.py** - AI-powered recommendation generation

### Data Flow Architecture

```
User Input (habit text) 
    ↓
NLP Categorizer (categorizes into: transport, energy, waste, water, consumption, food)
    ↓
Scoring System (calculates impact score with category weights + difficulty multipliers)
    ↓
Storage (in-memory list for demo, designed for database integration)
    ↓
Analytics & Suggestions (pattern analysis → personalized recommendations)
```

### Configuration System

The app uses a three-tier configuration system via `config/config.py`:
- **DevelopmentConfig** - Debug enabled, SQLite, verbose logging
- **ProductionConfig** - Security features, environment-based secrets
- **TestingConfig** - In-memory database, minimal logging

Configuration is selected via `FLASK_ENV` environment variable.

### Scoring Algorithm

The scoring system uses a weighted approach:
- **Base category weights**: transport(25), food(22), energy(20), consumption(18), waste(15), water(12)
- **Difficulty multipliers**: consumption(1.3x), transport(1.2x), food(1.1x), waste(1.0x), water(0.9x), energy(0.8x)
- **Intensity analysis**: Text analysis for effort indicators (1.2x multiplier range)

### NLP Categorization Strategy

Uses keyword matching + regex patterns approach:
- **Keywords**: Direct term matching for each category
- **Patterns**: Regex patterns for context-aware matching (weighted 2x)
- **Fallback**: "other" category for unmatched habits

Categories are scored and the highest-scoring category is selected.

## Environment Variables

Key environment variables for configuration:

```bash
# Flask settings
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=false
FLASK_ENV=development  # development/production/testing

# Database (for future use)
DATABASE_URL=sqlite:///habits.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/logs/app.log

# Feature flags
ENABLE_ANALYTICS=true
ENABLE_SUGGESTIONS=true
ENABLE_NOTIFICATIONS=false

# Security (production only)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

## Data Models

### Habit Entry Structure
```json
{
  "id": 1,
  "text": "took the bus to work instead of driving",
  "category": "transport",
  "impact_score": 30.0,
  "timestamp": "2024-01-15T09:30:00Z"
}
```

### Categories System
- **transport**: Public transit, walking, biking, carpooling
- **energy**: Conservation, efficient appliances, renewable energy
- **waste**: Recycling, composting, reusing, reducing
- **water**: Conservation, efficiency, leak fixing
- **consumption**: Local/organic purchasing, secondhand, repairs
- **food**: Plant-based meals, local produce, reduced waste

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/habits` - Log new habit
- `GET /api/habits` - Retrieve all habits
- `GET /api/score` - Get green score with breakdown
- `GET /api/suggestions` - Get AI recommendations
- `GET /api/stats` - Get comprehensive statistics

## Development Notes

### Database Integration
Currently uses in-memory storage (`habits_log = []`). For production:
- Database models are designed in configuration
- SQLAlchemy setup is prepared
- Migration path exists via `config.get_database_path()`

### AI/ML Components
- **NLP Categorizer**: Rule-based system, extensible to ML models
- **Scoring System**: Algorithmic with statistical analysis features
- **Suggestions Engine**: Template-based with user pattern analysis

### Testing Strategy
- Unit tests should cover each core component independently
- Integration tests for API endpoints
- Mock external dependencies in tests
- Use `TestingConfig` for isolated test runs

### Extension Points
- **New categories**: Add to `categories` dict in `HabitCategorizer`
- **Scoring adjustments**: Modify weights in `GreenScorer.__init__`
- **New suggestions**: Add templates to `suggestions_database` in `SuggestionsEngine`
- **Analytics**: Extend statistical functions in `scoring_system.py`

## Common Development Patterns

### Adding New Habit Categories
1. Update `nlp_categorizer.py` categories dict with keywords/patterns
2. Add category weight to `scoring_system.py`
3. Add suggestion templates to `suggestions_engine.py`
4. Update sample data in `data/sample_habits.json`

### Extending API Endpoints
Follow the established pattern:
- Add route decorator with appropriate HTTP method
- Include comprehensive error handling with try/catch
- Return JSON responses with consistent structure
- Log important operations for debugging

### Configuration Management
Use the config system for all environment-specific values:
- Add new settings to `Config` class
- Override in environment-specific subclasses as needed
- Access via `config('KEY', default=value)` pattern
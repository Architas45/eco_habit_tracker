# AI Green Habit Tracker

## Problem
Sustainable living is hard to track. People want to make environmentally conscious choices but struggle to understand the cumulative impact of their daily habits and lack personalized guidance for improvement.

## Solution
The AI Green Habit Tracker allows users to log their daily eco-friendly habits (such as "used public transport", "carpooled", "carried reusable bag") and leverages AI to provide:

- **Green Score**: An intelligent scoring system that quantifies environmental impact
- **Smart Suggestions**: AI-powered recommendations for improving sustainability
- **Progress Tracking**: Visual analytics showing environmental impact over time

## Key Features

### 🌱 Habit Logging
- Simple text input for daily green activities
- Natural language processing for automatic categorization
- Support for various eco-friendly behaviors (transport, energy, waste, etc.)

### 🤖 AI-Powered Analysis
- **NLP Categorization**: Automatically categorizes user inputs into environmental domains
- **Smart Scoring**: Calculates personalized green scores based on habit impact
- **Intelligent Suggestions**: Provides tailored recommendations for improvement

### 📊 Analytics & Insights
- Track progress over time
- Compare scores across different habit categories
- Identify trends and patterns in sustainable behavior

## Technology Stack

- **Backend**: Python with Flask/FastAPI
- **AI/ML**: scikit-learn, NLTK, spaCy for NLP processing
- **Data**: pandas, numpy for data analysis
- **Storage**: SQLite for development, PostgreSQL for production
- **API**: RESTful API design

## Project Structure

```
ai-green-habit-tracker/
├── src/                    # Core application code
│   ├── habit_tracker.py    # Main application entry point
│   ├── nlp_categorizer.py  # NLP processing and categorization
│   ├── scoring_system.py   # Green score calculation engine
│   └── suggestions_engine.py # AI recommendation system
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── data/                   # Sample data and datasets
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
└── setup.py               # Package setup
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-green-habit-tracker
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/habit_tracker.py
   ```

## API Usage Examples

### Log a Habit
```bash
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d '{"habit": "took the bus to work instead of driving"}'
```

### Get Green Score
```bash
curl http://localhost:5000/api/score
```

### Get Suggestions
```bash
curl http://localhost:5000/api/suggestions
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. Format code using:
```bash
black src/
flake8 src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Basic habit logging and NLP categorization
- [ ] Scoring system implementation
- [ ] AI suggestion engine
- [ ] Web interface
- [ ] Mobile app support
- [ ] Social features (sharing scores, challenges)
- [ ] Integration with IoT devices (smart home, fitness trackers)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have questions or need help, please open an issue on GitHub or contact the maintainers.

---

**Let's make sustainable living easier to track and improve! 🌍**
#!/usr/bin/env python3
"""
AI Green Habit Tracker - Main Application

This is the main entry point for the AI Green Habit Tracker application.
It provides a Flask API for logging habits, getting green scores, and receiving AI suggestions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os
import sys

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_categorizer import HabitCategorizer
from scoring_system import GreenScorer
from suggestions_engine import SuggestionsEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize AI components
categorizer = HabitCategorizer()
scorer = GreenScorer()
suggestions_engine = SuggestionsEngine()

# In-memory storage for demo (replace with database in production)
habits_log = []

def get_recommendation(category, habit):
    if category == "electricity":
        return {
            "impact_score": 17,
            "recommendation": "Switch off unused lights, use LED bulbs, and avoid standby power."
        }

    elif category == "energy":
        return {
            "impact_score": 20,
            "recommendation": "Use 5-star rated appliances and optimize energy usage during peak hours."
        }

    elif category == "water":
        return {
            "impact_score": 15,
            "recommendation": "Fix leaks and reuse water where possible."
        }

    elif category == "transport":
        return {
            "impact_score": 18,
            "recommendation": "Use public transport or carpool to reduce fuel consumption."
        }

    elif category == "waste":
        return {
            "impact_score": 14,
            "recommendation": "Segregate waste and compost biodegradable materials."
        }

    elif category == "agriculture":
        return {
            "impact_score": 22,
            "recommendation": "Use drip irrigation and organic farming practices."
        }

    else:
        return {
            "impact_score": 10,
            "recommendation": "Adopt general sustainable practices."
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0'
    })


@app.route('/api/habits', methods=['POST'])
def log_habit():
    """
    Log a new green habit.
    
    Expected JSON payload:
    {
        "habit": "took the bus to work instead of driving"
    }
    """
    try:
        data = request.get_json()
        if not data or 'habit' not in data:
            return jsonify({'error': 'Missing habit description'}), 400
        
        habit_text = data['habit'].strip()
        if not habit_text:
            return jsonify({'error': 'Habit description cannot be empty'}), 400
        
        # Process the habit
        category = categorizer.categorize(habit_text)
        impact_score = scorer.calculate_impact(habit_text, category)
        
        # Create habit entry
        habit_entry = {
            'id': len(habits_log) + 1,
            'text': habit_text,
            'category': category,
            'impact_score': impact_score,
            'timestamp': datetime.now().isoformat()
        }
        
        habits_log.append(habit_entry)
        
        logger.info(f"Logged habit: {habit_text} -> Category: {category}, Score: {impact_score}")
        
        return jsonify({
            'message': 'Habit logged successfully',
            'habit': habit_entry
        }), 201
        
    except Exception as e:
        logger.error(f"Error logging habit: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/habits', methods=['GET'])
def get_habits():
    """Get all logged habits."""
    return jsonify({
        'habits': habits_log,
        'count': len(habits_log)
    })


@app.route('/api/score', methods=['GET'])
def get_green_score():
    """Get the user's current green score."""
    try:
        if not habits_log:
            return jsonify({
                'green_score': 0,
                'total_habits': 0,
                'message': 'No habits logged yet'
            })
        
        total_score = scorer.calculate_total_score(habits_log)
        avg_score = total_score / len(habits_log) if habits_log else 0
        
        return jsonify({
            'green_score': round(avg_score, 2),
            'total_score': round(total_score, 2),
            'total_habits': len(habits_log),
            'score_breakdown': scorer.get_score_breakdown(habits_log)
        })
        
    except Exception as e:
        logger.error(f"Error calculating green score: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get AI-powered suggestions for improving green score."""
    try:
        suggestions = suggestions_engine.generate_suggestions(habits_log)
        
        return jsonify({
            'suggestions': suggestions,
            'personalized': len(habits_log) > 0
        })
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get comprehensive statistics about user's green habits."""
    try:
        if not habits_log:
            return jsonify({
                'message': 'No habits logged yet',
                'stats': {}
            })
        
        stats = {
            'total_habits': len(habits_log),
            'categories': categorizer.get_category_distribution(habits_log),
            'avg_daily_score': scorer.get_average_daily_score(habits_log),
            'improvement_trend': scorer.get_improvement_trend(habits_log),
            'top_habits': scorer.get_top_habits(habits_log),
        }
        
        return jsonify({
            'stats': stats,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating statistics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

from flask import Flask, request, jsonify

@app.route("/api/agriculture/tips", methods=["GET"])
def agriculture_tips():
    tips = [
        "Use drip irrigation to reduce water wastage",
        "Practice crop rotation to improve soil fertility",
        "Use organic fertilizers instead of chemical ones",
        "Harvest rainwater for irrigation",
        "Adopt solar-powered pumps in farms"
    ]
    return jsonify({
        "category": "agriculture",
        "tips": tips
    })

@app.route("/api/agriculture/recommend", methods=["POST"])
def recommend_agriculture():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    crop = data.get("crop")

    if not crop:
        return jsonify({"error": "Crop is required"}), 400

    crop = crop.lower()

    recommendations = {
        "rice": "Use alternate wetting and drying irrigation to save water",
        "wheat": "Adopt crop rotation and organic fertilizers to improve soil health",
        "vegetables": "Use drip irrigation and compost-based manure",
        "cotton": "Practice integrated pest management to reduce pesticides",
        "sugarcane": "Use mulching and controlled irrigation techniques"
    }

    return jsonify({
        "crop": crop,
        "recommendation": recommendations.get(
            crop,
            "Adopt sustainable and water-efficient farming practices"
        )
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Main function to run the application."""
    logger.info("Starting AI Green Habit Tracker...")
    
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Server starting on http://{host}:{port}")
    logger.info("Available endpoints:")
    logger.info("  POST /api/habits - Log a new habit")
    logger.info("  GET  /api/habits - Get all habits")
    logger.info("  GET  /api/score - Get green score")
    logger.info("  GET  /api/suggestions - Get AI suggestions")
    logger.info("  GET  /api/stats - Get statistics")
    logger.info("  GET  /api/health - Health check")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    app.run(port=5001, debug=True)

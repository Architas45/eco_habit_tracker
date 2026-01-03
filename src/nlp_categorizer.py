"""
NLP Categorizer for Green Habits

This module handles the natural language processing and categorization
of user-inputted green habits into environmental categories.
"""

import re
from typing import Dict, List, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class HabitCategorizer:
    """
    Categorizes green habits using NLP techniques.
    
    Categories:
    - transport: Public transport, walking, cycling, carpooling
    - energy: Energy conservation, renewable energy use
    - waste: Recycling, composting, waste reduction
    - water: Water conservation, efficient usage
    - consumption: Sustainable purchasing, local products
    - food: Plant-based meals, local food, reduced meat
    """
    
    def __init__(self):
        self.categories = {
            'transport': {
                'keywords': [
                    'bus', 'train', 'subway', 'metro', 'public transport', 'walk', 'walking',
                    'bike', 'bicycle', 'cycling', 'carpool', 'rideshare', 'electric car',
                    'hybrid', 'scooter', 'skateboard', 'work from home', 'remote work',
                    'telecommute', 'no driving', 'stayed home'
                ],
                'patterns': [
                    r'took.*bus', r'rode.*bike', r'walked.*work', r'carpooled.*with',
                    r'used.*public.*transport', r'avoided.*driving', r'no.*car.*today'
                ]
            },
            'energy': {
                'keywords': [
                    'lights', 'electricity', 'power', 'solar', 'energy', 'LED', 'efficient',
                    'thermostat', 'heating', 'cooling', 'unplug', 'battery', 'renewable',
                    'turned off', 'switched off', 'energy saving', 'power strip'
                ],
                'patterns': [
                    r'turned.*off.*lights', r'unplugged.*devices', r'used.*solar',
                    r'lowered.*thermostat', r'energy.*efficient', r'saved.*electricity'
                ]
            },
            'waste': {
                'keywords': [
                    'recycle', 'recycling', 'compost', 'composting', 'reuse', 'reusable',
                    'bag', 'bottle', 'container', 'plastic', 'paper', 'glass', 'metal',
                    'trash', 'garbage', 'waste', 'reduce', 'minimal packaging'
                ],
                'patterns': [
                    r'recycled.*bottles', r'composted.*food', r'reusable.*bag',
                    r'avoided.*plastic', r'brought.*own.*bag', r'no.*disposable'
                ]
            },
            'water': {
                'keywords': [
                    'water', 'shower', 'tap', 'faucet', 'leak', 'rain', 'collected',
                    'conservation', 'efficient', 'low flow', 'drought', 'watering'
                ],
                'patterns': [
                    r'shorter.*shower', r'fixed.*leak', r'collected.*rainwater',
                    r'watered.*garden.*with.*greywater', r'turned.*off.*tap'
                ]
            },
            'consumption': {
                'keywords': [
                    'local', 'organic', 'sustainable', 'eco-friendly', 'green product',
                    'second-hand', 'thrift', 'used', 'repair', 'fix', 'vintage',
                    'handmade', 'artisan', 'fair trade', 'ethical'
                ],
                'patterns': [
                    r'bought.*local', r'purchased.*organic', r'thrift.*shopping',
                    r'repaired.*instead.*buying', r'second.*hand.*store'
                ]
            },
            'food': {
                'keywords': [
                    'vegetarian', 'vegan', 'plant-based', 'meatless', 'local food',
                    'farmers market', 'homegrown', 'garden', 'grew', 'organic food',
                    'seasonal', 'no meat', 'plant protein', 'vegetables', 'fruits'
                ],
                'patterns': [
                    r'ate.*vegetarian', r'cooked.*plant.*based', r'meatless.*monday',
                    r'farmers.*market', r'grew.*own.*vegetables', r'no.*meat.*today'
                ]
            }
        }
    
    def categorize(self, habit_text: str) -> str:
        """
        Categorize a habit text into one of the environmental categories.
        
        Args:
            habit_text: The user's habit description
            
        Returns:
            Category name or 'other' if no match found
        """
        habit_lower = habit_text.lower()
        category_scores = {}
        
        # Score each category based on keyword and pattern matches
        for category, config in self.categories.items():
            score = 0
            
            # Check for keyword matches
            for keyword in config['keywords']:
                if keyword in habit_lower:
                    score += 1
            
            # Check for pattern matches (weighted higher)
            for pattern in config['patterns']:
                if re.search(pattern, habit_lower):
                    score += 2
            
            if score > 0:
                category_scores[category] = score
        
        # Return the highest scoring category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            logger.info(f"Categorized '{habit_text}' as '{best_category}' (score: {category_scores[best_category]})")
            return best_category
        else:
            logger.info(f"Could not categorize '{habit_text}', defaulting to 'other'")
            return 'other'
    
    def get_category_distribution(self, habits_log: List[Dict]) -> Dict[str, int]:
        """
        Get the distribution of habits across categories.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Dictionary with category counts
        """
        if not habits_log:
            return {}
        
        categories = [habit.get('category', 'other') for habit in habits_log]
        return dict(Counter(categories))
    
    def get_category_description(self, category: str) -> str:
        """
        Get a human-readable description of a category.
        
        Args:
            category: Category name
            
        Returns:
            Description string
        """
        descriptions = {
            'transport': 'Transportation & Mobility',
            'energy': 'Energy Conservation',
            'waste': 'Waste Reduction & Recycling',
            'water': 'Water Conservation',
            'consumption': 'Sustainable Consumption',
            'food': 'Food & Diet',
            'other': 'Other Environmental Actions'
        }
        return descriptions.get(category, 'Unknown Category')
    
    def suggest_category_improvements(self, habits_log: List[Dict]) -> List[str]:
        """
        Suggest categories where the user could improve their habits.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            List of improvement suggestions
        """
        if not habits_log:
            return [
                "Start logging your green habits to get personalized suggestions!",
                "Try focusing on transportation choices like walking or public transit.",
                "Consider energy conservation habits like turning off lights."
            ]
        
        distribution = self.get_category_distribution(habits_log)
        all_categories = set(self.categories.keys())
        logged_categories = set(distribution.keys()) - {'other'}
        missing_categories = all_categories - logged_categories
        
        suggestions = []
        
        # Suggest missing categories
        for category in missing_categories:
            if category == 'transport':
                suggestions.append("Try logging transportation habits like taking public transit or walking.")
            elif category == 'energy':
                suggestions.append("Consider tracking energy conservation actions like turning off lights.")
            elif category == 'waste':
                suggestions.append("Think about waste reduction habits like using reusable bags or recycling.")
            elif category == 'water':
                suggestions.append("Try water conservation habits like shorter showers or fixing leaks.")
            elif category == 'consumption':
                suggestions.append("Consider sustainable consumption choices like buying local or second-hand.")
            elif category == 'food':
                suggestions.append("Explore food-related habits like eating plant-based meals or shopping at farmers markets.")
        
        # Suggest improvements for underrepresented categories
        if distribution:
            min_count = min(distribution.values())
            underrepresented = [cat for cat, count in distribution.items() if count == min_count and cat != 'other']
            
            for category in underrepresented[:2]:  # Limit to top 2 suggestions
                suggestions.append(f"You could explore more {self.get_category_description(category).lower()} habits.")
        
        return suggestions[:3]  # Return top 3 suggestions
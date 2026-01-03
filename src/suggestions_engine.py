"""
AI Suggestions Engine

This module generates personalized suggestions for improving green habits
based on user's current patterns and environmental impact goals.
"""

from typing import Dict, List, Optional
from collections import defaultdict, Counter
import random
import logging

logger = logging.getLogger(__name__)


class SuggestionsEngine:
    """
    Generates AI-powered suggestions for improving environmental habits.
    
    The engine analyzes user patterns and provides personalized recommendations
    based on:
    - Current habit categories and gaps
    - Score optimization opportunities
    - Seasonal and contextual factors
    - Difficulty progression
    """
    
    def __init__(self):
        # Suggestion templates by category
        self.suggestions_database = {
            'transport': {
                'beginner': [
                    "Walk or bike for trips under 1 mile instead of driving",
                    "Try carpooling with a colleague or friend once this week",
                    "Use public transportation for at least one trip today",
                    "Combine multiple errands into one trip to reduce driving",
                    "Work from home one day this week if possible"
                ],
                'intermediate': [
                    "Plan a car-free day and use only walking, biking, or public transport",
                    "Join or organize a carpool group for your regular commute",
                    "Try an electric scooter or bike-share program",
                    "Walk or bike to nearby restaurants instead of driving",
                    "Use video calls instead of traveling for short meetings"
                ],
                'advanced': [
                    "Go car-free for an entire week and explore alternative transportation",
                    "Calculate your transportation carbon footprint and set reduction goals",
                    "Advocate for better bike lanes or public transport in your community",
                    "Consider switching to an electric or hybrid vehicle",
                    "Plan a local vacation that doesn't require flying"
                ]
            },
            'energy': {
                'beginner': [
                    "Turn off lights when leaving a room",
                    "Unplug devices and chargers when not in use",
                    "Set your thermostat 2 degrees lower in winter",
                    "Use a programmable thermostat to optimize heating/cooling",
                    "Switch to LED light bulbs in your most-used rooms"
                ],
                'intermediate': [
                    "Air dry your clothes instead of using the dryer",
                    "Use a power strip to easily turn off multiple devices at once",
                    "Seal air leaks around windows and doors",
                    "Use ceiling fans to reduce air conditioning needs",
                    "Only run dishwashers and washing machines with full loads"
                ],
                'advanced': [
                    "Install a smart thermostat to optimize energy usage",
                    "Consider switching to renewable energy from your utility provider",
                    "Install solar panels or explore community solar options",
                    "Conduct a home energy audit to identify efficiency improvements",
                    "Upgrade to energy-efficient appliances when replacing old ones"
                ]
            },
            'waste': {
                'beginner': [
                    "Bring a reusable bag when grocery shopping",
                    "Start recycling paper, plastic, and glass containers",
                    "Use a reusable water bottle instead of buying bottled water",
                    "Repurpose glass jars for food storage",
                    "Donate items you no longer need instead of throwing them away"
                ],
                'intermediate': [
                    "Start composting food scraps and yard waste",
                    "Buy products with minimal or recyclable packaging",
                    "Use both sides of paper before recycling it",
                    "Repair items instead of immediately replacing them",
                    "Organize a clothing swap with friends or neighbors"
                ],
                'advanced': [
                    "Aim for zero waste by refusing, reducing, reusing, and recycling",
                    "Make your own cleaning products from natural ingredients",
                    "Start vermicomposting (composting with worms)",
                    "Buy only what you need and choose quality over quantity",
                    "Participate in or organize community cleanup events"
                ]
            },
            'water': {
                'beginner': [
                    "Take shorter showers (aim for 5 minutes or less)",
                    "Turn off the tap while brushing teeth or washing dishes",
                    "Fix any leaky faucets or running toilets promptly",
                    "Only run the washing machine with full loads",
                    "Use a dishwasher instead of hand washing when possible"
                ],
                'intermediate': [
                    "Install low-flow showerheads and faucet aerators",
                    "Collect rainwater for watering plants and garden",
                    "Use drought-resistant plants in your landscaping",
                    "Take navy showers (water on to wet, off to soap, on to rinse)",
                    "Reuse greywater from showers for watering plants"
                ],
                'advanced': [
                    "Install a greywater recycling system for your home",
                    "Use permeable paving materials to reduce runoff",
                    "Create a rain garden to manage stormwater naturally",
                    "Install a smart irrigation system that adjusts to weather",
                    "Advocate for water conservation policies in your community"
                ]
            },
            'consumption': {
                'beginner': [
                    "Buy one item from a local farmer's market or local business",
                    "Choose products made from recycled materials",
                    "Buy only what you need and avoid impulse purchases",
                    "Look for the Energy Star label when buying appliances",
                    "Choose quality items that will last longer over cheap alternatives"
                ],
                'intermediate': [
                    "Shop at thrift stores or consignment shops for clothing",
                    "Buy organic or sustainably produced food when possible",
                    "Support businesses with strong environmental commitments",
                    "Choose digital receipts and bills instead of paper",
                    "Research a company's sustainability practices before purchasing"
                ],
                'advanced': [
                    "Adopt a minimalist lifestyle and buy only essentials",
                    "Invest in renewable energy or sustainable companies",
                    "Support local and regenerative agriculture practices",
                    "Choose products with closed-loop or circular design",
                    "Advocate for sustainable business practices in your community"
                ]
            },
            'food': {
                'beginner': [
                    "Have one plant-based meal today",
                    "Buy one locally grown fruit or vegetable",
                    "Reduce food waste by meal planning for the week",
                    "Start or expand an herb garden (even on a windowsill)",
                    "Choose organic options for the 'dirty dozen' produce items"
                ],
                'intermediate': [
                    "Try 'Meatless Monday' or have several plant-based meals this week",
                    "Compost food scraps to reduce waste and create fertilizer",
                    "Shop at a farmer's market for seasonal, local produce",
                    "Grow your own vegetables in a garden or containers",
                    "Preserve seasonal produce by freezing, canning, or dehydrating"
                ],
                'advanced': [
                    "Adopt a predominantly plant-based diet",
                    "Source most of your food from local and organic producers",
                    "Practice regenerative eating by supporting sustainable farming",
                    "Participate in community supported agriculture (CSA)",
                    "Teach others about sustainable food choices and preparation"
                ]
            }
        }
        
        # Seasonal suggestions (for more contextual recommendations)
        self.seasonal_suggestions = {
            'spring': [
                "Start a vegetable garden with spring crops like lettuce and peas",
                "Use a rain barrel to collect water for gardening",
                "Walk or bike more as the weather gets warmer",
                "Spring clean by donating items you no longer need"
            ],
            'summer': [
                "Use fans instead of air conditioning when possible",
                "Hang dry clothes outside in the sunshine",
                "Eat more fresh, local produce that's in season",
                "Take advantage of longer days to walk or bike more"
            ],
            'fall': [
                "Compost fallen leaves and plant matter",
                "Preserve seasonal produce by canning or freezing",
                "Adjust your thermostat as temperatures cool down",
                "Buy local apples, squash, and other fall crops"
            ],
            'winter': [
                "Lower your thermostat and wear warmer clothes indoors",
                "Use draft stoppers to keep warm air in",
                "Plan meals using preserved foods from summer and fall",
                "Consider indoor composting if outdoor composting isn't possible"
            ]
        }
        
        # Challenge suggestions for engaged users
        self.challenges = [
            "Zero Waste Week: Try to produce no landfill waste for 7 days",
            "Car-Free Week: Use only walking, biking, and public transport",
            "Energy Diet: Reduce your electricity usage by 20% this month",
            "Local Food Challenge: Eat only locally sourced food for a week",
            "Plant-Based Week: Eat only plant-based meals for 7 days",
            "Repair Week: Fix or repurpose items instead of buying new ones",
            "Water Conservation Challenge: Reduce water usage by 25% this month",
            "Plastic-Free Week: Avoid single-use plastics for 7 days"
        ]
    
    def generate_suggestions(self, habits_log: List[Dict]) -> List[Dict]:
        """
        Generate personalized suggestions based on user's habit history.
        
        Args:
            habits_log: List of user's logged habits
            
        Returns:
            List of suggestion dictionaries with text, category, and difficulty
        """
        if not habits_log:
            return self._get_beginner_suggestions()
        
        suggestions = []
        
        # Analyze user's current patterns
        user_analysis = self._analyze_user_patterns(habits_log)
        
        # Get category-based suggestions
        suggestions.extend(self._get_category_suggestions(user_analysis))
        
        # Add improvement suggestions based on current scores
        suggestions.extend(self._get_improvement_suggestions(habits_log, user_analysis))
        
        # Add challenge suggestions for experienced users
        if len(habits_log) >= 20:  # User has logged many habits
            suggestions.extend(self._get_challenge_suggestions())
        
        # Add seasonal suggestions
        suggestions.extend(self._get_seasonal_suggestions())
        
        # Limit and randomize suggestions
        return self._finalize_suggestions(suggestions)
    
    def _get_beginner_suggestions(self) -> List[Dict]:
        """Get suggestions for users who haven't logged any habits yet."""
        suggestions = []
        
        # Get one beginner suggestion from each major category
        for category in ['transport', 'energy', 'waste', 'food']:
            suggestion_text = random.choice(self.suggestions_database[category]['beginner'])
            suggestions.append({
                'text': suggestion_text,
                'category': category,
                'difficulty': 'beginner',
                'reason': 'Great starting point for sustainable habits'
            })
        
        return suggestions
    
    def _analyze_user_patterns(self, habits_log: List[Dict]) -> Dict:
        """Analyze user's habit patterns to inform suggestions."""
        categories = [habit.get('category', 'other') for habit in habits_log]
        category_counts = Counter(categories)
        
        # Calculate user level based on habit count
        total_habits = len(habits_log)
        if total_habits < 5:
            user_level = 'beginner'
        elif total_habits < 20:
            user_level = 'intermediate'
        else:
            user_level = 'advanced'
        
        # Find underrepresented categories
        all_categories = set(self.suggestions_database.keys())
        active_categories = set(category_counts.keys()) - {'other'}
        missing_categories = all_categories - active_categories
        
        # Find categories with low activity
        avg_count = sum(category_counts.values()) / len(category_counts) if category_counts else 0
        underrepresented = [cat for cat, count in category_counts.items() 
                          if count < avg_count and cat != 'other']
        
        return {
            'user_level': user_level,
            'category_counts': category_counts,
            'missing_categories': missing_categories,
            'underrepresented_categories': underrepresented,
            'total_habits': total_habits
        }
    
    def _get_category_suggestions(self, user_analysis: Dict) -> List[Dict]:
        """Get suggestions to fill gaps in habit categories."""
        suggestions = []
        user_level = user_analysis['user_level']
        
        # Suggest for completely missing categories
        for category in list(user_analysis['missing_categories'])[:2]:  # Limit to 2
            suggestion_text = random.choice(self.suggestions_database[category]['beginner'])
            suggestions.append({
                'text': suggestion_text,
                'category': category,
                'difficulty': 'beginner',
                'reason': f'Explore {category.title()} habits to diversify your environmental impact'
            })
        
        # Suggest for underrepresented categories
        for category in list(user_analysis['underrepresented_categories'])[:1]:  # Limit to 1
            suggestion_text = random.choice(self.suggestions_database[category][user_level])
            suggestions.append({
                'text': suggestion_text,
                'category': category,
                'difficulty': user_level,
                'reason': f'Build on your {category.title().lower()} habits'
            })
        
        return suggestions
    
    def _get_improvement_suggestions(self, habits_log: List[Dict], user_analysis: Dict) -> List[Dict]:
        """Get suggestions for improving existing habit categories."""
        suggestions = []
        user_level = user_analysis['user_level']
        
        # Find the user's most active categories
        top_categories = sorted(
            user_analysis['category_counts'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]  # Top 2 categories
        
        for category, count in top_categories:
            if category in self.suggestions_database:
                # Suggest advancing to next level in their strong categories
                next_level = {
                    'beginner': 'intermediate',
                    'intermediate': 'advanced',
                    'advanced': 'advanced'  # Stay at advanced
                }[user_level]
                
                suggestion_text = random.choice(self.suggestions_database[category][next_level])
                suggestions.append({
                    'text': suggestion_text,
                    'category': category,
                    'difficulty': next_level,
                    'reason': f'Level up your {category.title().lower()} habits'
                })
        
        return suggestions
    
    def _get_challenge_suggestions(self) -> List[Dict]:
        """Get challenge suggestions for experienced users."""
        challenge = random.choice(self.challenges)
        
        return [{
            'text': challenge,
            'category': 'challenge',
            'difficulty': 'advanced',
            'reason': 'Take on a sustainability challenge to deepen your impact'
        }]
    
    def _get_seasonal_suggestions(self) -> List[Dict]:
        """Get suggestions based on current season."""
        # Simple season detection based on month (Northern Hemisphere)
        import datetime
        month = datetime.datetime.now().month
        
        if month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        elif month in [9, 10, 11]:
            season = 'fall'
        else:
            season = 'winter'
        
        suggestion_text = random.choice(self.seasonal_suggestions[season])
        
        return [{
            'text': suggestion_text,
            'category': 'seasonal',
            'difficulty': 'intermediate',
            'reason': f'Seasonal suggestion for {season.title()}'
        }]
    
    def _finalize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Finalize suggestions by removing duplicates and limiting count."""
        # Remove duplicates based on text
        seen_texts = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            if suggestion['text'] not in seen_texts:
                seen_texts.add(suggestion['text'])
                unique_suggestions.append(suggestion)
        
        # Shuffle and limit to 5-7 suggestions
        random.shuffle(unique_suggestions)
        return unique_suggestions[:random.randint(5, 7)]
    
    def get_suggestion_explanation(self, suggestion_text: str) -> str:
        """Get a detailed explanation of why a suggestion is beneficial."""
        explanations = {
            'transport': "Transportation is one of the largest sources of greenhouse gas emissions. Choosing sustainable transport options like walking, biking, or public transit significantly reduces your carbon footprint.",
            'energy': "Energy consumption in homes accounts for a significant portion of carbon emissions. Reducing energy use and switching to renewable sources helps combat climate change.",
            'waste': "Waste reduction through reuse, recycling, and composting helps conserve natural resources and reduces pollution from landfills and incineration.",
            'water': "Water conservation helps protect this precious resource and reduces energy consumption required for water processing and heating.",
            'consumption': "Conscious consumption choices support sustainable businesses and reduce the environmental impact of manufacturing and transportation.",
            'food': "Food production has major environmental impacts. Plant-based and local foods typically require less water, land, and energy while producing fewer emissions."
        }
        
        # Try to match suggestion to category
        for category, explanation in explanations.items():
            if any(keyword in suggestion_text.lower() for keyword in self._get_category_keywords(category)):
                return explanation
        
        return "This habit helps reduce your environmental impact and contributes to a more sustainable lifestyle."
    
    def _get_category_keywords(self, category: str) -> List[str]:
        """Get keywords associated with each category for matching."""
        keywords = {
            'transport': ['walk', 'bike', 'bus', 'train', 'drive', 'car', 'transport', 'commute'],
            'energy': ['energy', 'electricity', 'power', 'lights', 'thermostat', 'heating', 'cooling'],
            'waste': ['waste', 'recycle', 'compost', 'reuse', 'bag', 'plastic', 'trash'],
            'water': ['water', 'shower', 'tap', 'leak', 'rain', 'irrigation'],
            'consumption': ['buy', 'purchase', 'local', 'organic', 'sustainable', 'shop'],
            'food': ['food', 'eat', 'plant', 'meat', 'vegetarian', 'vegan', 'organic', 'local']
        }
        
        return keywords.get(category, [])

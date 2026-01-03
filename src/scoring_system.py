"""
Green Scoring System

This module calculates environmental impact scores for green habits
and provides analytics on user's sustainability progress.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import logging

logger = logging.getLogger(__name__)


class GreenScorer:
    """
    Calculates and tracks green scores for environmental habits.
    
    Scoring is based on:
    - Category impact weight
    - Habit frequency
    - Environmental benefit scale
    - User consistency
    """
    
    def __init__(self):
        # Base impact scores for each category (0-100)
        self.category_weights = {
            'transport': 25,      # High impact: reduces emissions significantly
            'energy': 20,         # High impact: energy conservation
            'waste': 15,          # Medium-high impact: waste reduction
            'water': 12,          # Medium impact: water conservation
            'consumption': 18,    # High impact: sustainable purchasing
            'food': 22,           # High impact: diet choices
            'other': 8            # Lower impact: general environmental actions
        }
        
        # Habit difficulty multipliers (easier habits get less points)
        self.difficulty_multipliers = {
            'transport': 1.2,     # Often requires planning/effort
            'energy': 0.8,        # Usually simple actions
            'waste': 1.0,         # Moderate effort
            'water': 0.9,         # Usually simple actions
            'consumption': 1.3,   # Requires research/planning
            'food': 1.1,          # Some planning required
            'other': 1.0          # Variable difficulty
        }
    
    def calculate_impact(self, habit_text: str, category: str) -> float:
        """
        Calculate the environmental impact score for a single habit.
        
        Args:
            habit_text: Description of the habit
            category: Habit category
            
        Returns:
            Impact score (0-100)
        """
        base_score = self.category_weights.get(category, 10)
        difficulty_multiplier = self.difficulty_multipliers.get(category, 1.0)
        
        # Analyze habit text for intensity indicators
        intensity_multiplier = self._analyze_habit_intensity(habit_text)
        
        # Calculate final score
        score = base_score * difficulty_multiplier * intensity_multiplier
        
        # Cap at 100 and round
        final_score = min(100, round(score, 1))
        
        logger.info(f"Calculated impact for '{habit_text}': {final_score} (base: {base_score}, difficulty: {difficulty_multiplier}, intensity: {intensity_multiplier})")
        
        return final_score
    
    def _analyze_habit_intensity(self, habit_text: str) -> float:
        """
        Analyze the habit text to determine intensity/effort level.
        
        Args:
            habit_text: Description of the habit
            
        Returns:
            Intensity multiplier (0.5 - 1.5)
        """
        text_lower = habit_text.lower()
        multiplier = 1.0
        
        # High-effort indicators
        high_effort_terms = [
            'all day', 'entire', 'completely', 'totally', 'exclusively',
            'walked to', 'biked to', 'cycled to', 'carpooled with',
            'organized', 'planned', 'researched', 'installed'
        ]
        
        # Low-effort indicators  
        low_effort_terms = [
            'just', 'simply', 'only', 'briefly', 'quickly',
            'remembered to', 'tried to', 'attempted'
        ]
        
        # Duration indicators
        duration_high = ['hour', 'hours', 'day', 'week', 'month']
        duration_low = ['minute', 'minutes', 'second', 'moment']
        
        # Check for high-effort terms
        for term in high_effort_terms:
            if term in text_lower:
                multiplier += 0.2
                break
        
        # Check for low-effort terms
        for term in low_effort_terms:
            if term in text_lower:
                multiplier -= 0.2
                break
        
        # Check for duration indicators
        for term in duration_high:
            if term in text_lower:
                multiplier += 0.1
                break
                
        for term in duration_low:
            if term in text_lower:
                multiplier -= 0.1
                break
        
        # Ensure multiplier is within bounds
        return max(0.5, min(1.5, multiplier))
    
    def calculate_total_score(self, habits_log: List[Dict]) -> float:
        """
        Calculate the total green score from all habits.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Total score
        """
        if not habits_log:
            return 0.0
        
        total = sum(habit.get('impact_score', 0) for habit in habits_log)
        return round(total, 2)
    
    def get_score_breakdown(self, habits_log: List[Dict]) -> Dict[str, Dict]:
        """
        Get detailed score breakdown by category.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Dictionary with category breakdowns
        """
        if not habits_log:
            return {}
        
        breakdown = defaultdict(lambda: {'count': 0, 'total_score': 0, 'avg_score': 0})
        
        for habit in habits_log:
            category = habit.get('category', 'other')
            score = habit.get('impact_score', 0)
            
            breakdown[category]['count'] += 1
            breakdown[category]['total_score'] += score
        
        # Calculate averages
        for category, data in breakdown.items():
            if data['count'] > 0:
                data['avg_score'] = round(data['total_score'] / data['count'], 2)
                data['total_score'] = round(data['total_score'], 2)
        
        return dict(breakdown)
    
    def get_average_daily_score(self, habits_log: List[Dict]) -> float:
        """
        Calculate average daily green score.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Average daily score
        """
        if not habits_log:
            return 0.0
        
        # Group habits by date
        daily_scores = defaultdict(float)
        
        for habit in habits_log:
            timestamp = habit.get('timestamp', '')
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).date()
                    daily_scores[date] += habit.get('impact_score', 0)
                except (ValueError, AttributeError):
                    continue
        
        if not daily_scores:
            return 0.0
        
        avg_score = statistics.mean(daily_scores.values())
        return round(avg_score, 2)
    
    def get_improvement_trend(self, habits_log: List[Dict]) -> Dict[str, float]:
        """
        Calculate improvement trend over time.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Dictionary with trend information
        """
        if len(habits_log) < 7:  # Need at least a week of data
            return {
                'trend': 'insufficient_data',
                'weekly_change': 0.0,
                'trend_percentage': 0.0
            }
        
        # Sort habits by timestamp
        sorted_habits = sorted(
            habits_log,
            key=lambda h: h.get('timestamp', ''),
            reverse=False
        )
        
        # Split into first and second half
        mid_point = len(sorted_habits) // 2
        first_half = sorted_habits[:mid_point]
        second_half = sorted_habits[mid_point:]
        
        # Calculate average scores for each half
        first_avg = statistics.mean([h.get('impact_score', 0) for h in first_half])
        second_avg = statistics.mean([h.get('impact_score', 0) for h in second_half])
        
        # Calculate trend
        change = second_avg - first_avg
        percentage_change = (change / first_avg * 100) if first_avg > 0 else 0
        
        trend_label = 'improving' if change > 1 else 'declining' if change < -1 else 'stable'
        
        return {
            'trend': trend_label,
            'weekly_change': round(change, 2),
            'trend_percentage': round(percentage_change, 1)
        }
    
    def get_top_habits(self, habits_log: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Get the top-scoring habits.
        
        Args:
            habits_log: List of habit entries
            limit: Maximum number of habits to return
            
        Returns:
            List of top habits
        """
        if not habits_log:
            return []
        
        # Sort by impact score (descending)
        sorted_habits = sorted(
            habits_log,
            key=lambda h: h.get('impact_score', 0),
            reverse=True
        )
        
        return sorted_habits[:limit]
    
    def get_consistency_score(self, habits_log: List[Dict]) -> Dict[str, float]:
        """
        Calculate consistency score based on habit frequency.
        
        Args:
            habits_log: List of habit entries
            
        Returns:
            Dictionary with consistency metrics
        """
        if not habits_log:
            return {
                'consistency_score': 0.0,
                'streak_days': 0,
                'total_days_active': 0
            }
        
        # Group habits by date
        daily_activity = set()
        
        for habit in habits_log:
            timestamp = habit.get('timestamp', '')
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).date()
                    daily_activity.add(date)
                except (ValueError, AttributeError):
                    continue
        
        if not daily_activity:
            return {
                'consistency_score': 0.0,
                'streak_days': 0,
                'total_days_active': 0
            }
        
        # Calculate consistency metrics
        total_days_active = len(daily_activity)
        
        # Calculate current streak
        sorted_dates = sorted(daily_activity, reverse=True)
        current_date = datetime.now().date()
        streak_days = 0
        
        for date in sorted_dates:
            if (current_date - date).days <= streak_days:
                streak_days += 1
                current_date = date - timedelta(days=1)
            else:
                break
        
        # Calculate overall consistency score (0-100)
        if len(habits_log) >= 7:  # Need at least a week for meaningful consistency
            days_span = (max(daily_activity) - min(daily_activity)).days + 1
            consistency_score = (total_days_active / days_span) * 100
        else:
            consistency_score = (streak_days / 7) * 100  # Based on current streak
        
        return {
            'consistency_score': round(min(100, consistency_score), 1),
            'streak_days': streak_days,
            'total_days_active': total_days_active
        }

"""
Configuration settings for AI Green Habit Tracker

This module contains configuration settings and environment variable handling
for the application.
"""

import os
from typing import Dict, Any
from decouple import config, Csv


class Config:
    """Base configuration class."""
    
    # Flask settings
    FLASK_HOST = config('FLASK_HOST', default='127.0.0.1')
    FLASK_PORT = config('FLASK_PORT', default=5000, cast=int)
    FLASK_DEBUG = config('FLASK_DEBUG', default=False, cast=bool)
    
    # Application settings
    APP_NAME = "AI Green Habit Tracker"
    APP_VERSION = "0.1.0"
    
    # Database settings (for future use)
    DATABASE_URL = config('DATABASE_URL', default='sqlite:///habits.db')
    
    # Logging settings
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')
    LOG_FILE = config('LOG_FILE', default='data/logs/app.log')
    
    # AI/ML settings
    NLP_MODEL_PATH = config('NLP_MODEL_PATH', default='data/models/')
    SCORING_WEIGHTS = {
        'transport': 25,
        'energy': 20,
        'waste': 15,
        'water': 12,
        'consumption': 18,
        'food': 22,
        'other': 8
    }
    
    # API settings
    API_PREFIX = '/api'
    CORS_ORIGINS = config('CORS_ORIGINS', default='*', cast=Csv())
    
    # Security settings (for future use)
    SECRET_KEY = config('SECRET_KEY', default='dev-key-change-in-production')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='jwt-dev-key')
    
    # Feature flags
    ENABLE_ANALYTICS = config('ENABLE_ANALYTICS', default=True, cast=bool)
    ENABLE_SUGGESTIONS = config('ENABLE_SUGGESTIONS', default=True, cast=bool)
    ENABLE_NOTIFICATIONS = config('ENABLE_NOTIFICATIONS', default=False, cast=bool)
    
    # Rate limiting (for future use)
    RATE_LIMIT_ENABLED = config('RATE_LIMIT_ENABLED', default=False, cast=bool)
    RATE_LIMIT_REQUESTS = config('RATE_LIMIT_REQUESTS', default=100, cast=int)
    RATE_LIMIT_WINDOW = config('RATE_LIMIT_WINDOW', default=3600, cast=int)  # 1 hour
    
    @classmethod
    def get_database_path(cls) -> str:
        """Get the database file path for SQLite."""
        if cls.DATABASE_URL.startswith('sqlite:///'):
            db_path = cls.DATABASE_URL.replace('sqlite:///', '')
            # Ensure the directory exists
            os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
            return db_path
        return cls.DATABASE_URL
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        directories = [
            'data/logs',
            'data/models',
            'data/backups',
            os.path.dirname(cls.LOG_FILE) if os.path.dirname(cls.LOG_FILE) else 'data/logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)."""
        return {
            'app_name': cls.APP_NAME,
            'app_version': cls.APP_VERSION,
            'flask_host': cls.FLASK_HOST,
            'flask_port': cls.FLASK_PORT,
            'flask_debug': cls.FLASK_DEBUG,
            'log_level': cls.LOG_LEVEL,
            'enable_analytics': cls.ENABLE_ANALYTICS,
            'enable_suggestions': cls.ENABLE_SUGGESTIONS,
            'enable_notifications': cls.ENABLE_NOTIFICATIONS,
            'scoring_weights': cls.SCORING_WEIGHTS
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_DEBUG = True
    LOG_LEVEL = 'DEBUG'
    DATABASE_URL = config('DEV_DATABASE_URL', default='sqlite:///data/dev_habits.db')


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_DEBUG = False
    LOG_LEVEL = 'WARNING'
    DATABASE_URL = config('PROD_DATABASE_URL', default='sqlite:///data/habits.db')
    
    # Override with more secure defaults for production
    SECRET_KEY = config('SECRET_KEY', default=None)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default=None)
    
    # Enable security features in production
    RATE_LIMIT_ENABLED = True
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production")
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    FLASK_DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'  # In-memory database for tests
    LOG_LEVEL = 'ERROR'  # Reduce noise during testing
    
    # Disable external dependencies during testing
    ENABLE_ANALYTICS = False
    ENABLE_NOTIFICATIONS = False


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """
    Get configuration class based on environment.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Configuration class instance
    """
    if config_name is None:
        config_name = config('FLASK_ENV', default='development')
    
    config_class = config_map.get(config_name, config_map['default'])
    
    # Ensure required directories exist
    config_class.ensure_directories()
    
    return config_class()
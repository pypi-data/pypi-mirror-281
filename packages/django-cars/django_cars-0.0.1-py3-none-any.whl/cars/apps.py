"""
App configuration for the cars app.
"""

from django.apps import AppConfig


class CarsConfig(AppConfig):
    """
    Configuration class for the cars app.
    """
    name = 'cars'
    default_auto_field = 'django.db.models.BigAutoField'

"""
APIClient Plus - Production-ready resilient API client
"""

__version__ = "0.1.0"
__author__ = "Timox"
__email__ = "your.email@example.com"

# Импортируем основной класс и функции
from .client import APIClient, create_client, get_default_client

# Экспортируем для импорта
__all__ = [
    "APIClient",
    "create_client", 
    "get_default_client",
]
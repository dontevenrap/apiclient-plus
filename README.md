# APIClient Plus 🚀

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/dontevenrap/apiclient-plus.svg)](https://github.com/dontevenrap/apiclient-plus/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dontevenrap/apiclient-plus.svg)](https://github.com/dontevenrap/apiclient-plus/network)

Производственный Python-клиент для работы с внешними API. Автоматически переключается между разными источниками при ошибках, кэширует результаты и предоставляет статистику использования.

## ✨ Возможности

- ✅ **Автоматическое переключение** между API источниками
- ✅ **Умные повторные попытки** с экспоненциальной задержкой
- ✅ **Встроенное кэширование** с TTL (время жизни)
- ✅ **Подробная статистика** использования API
- ✅ **3 готовых API**: Цена Bitcoin, погода, курсы валют
- ✅ **Простой и понятный** интерфейс

## 📦 Установка

```bash
# Установка через pip
pip install git+https://github.com/dontevenrap/apiclient-plus.git
```

Или установите из исходников:

```bash
git clone https://github.com/dontevenrap/apiclient-plus.git
cd apiclient-plus
pip install -e .
```

🚀 Быстрый старт

Пример 1: Получить цену Bitcoin

```bash
from apiclient import APIClient

client = APIClient()
result = client.get_bitcoin_price()

if result["success"]:
    print(f"💰 Bitcoin: ${result['price']:,.2f}")
# Вывод: Bitcoin: $85,955.00
```

Пример 2: Получить погоду

```bash
weather = client.get_weather("London")
if weather["success"]:
    print(f"🌤️ London: {weather['temperature']}°C, {weather['description']}")
# Вывод: London: 11.6°C, Weather code: 3
```

Пример 3: Получить курс валют

```bash
exchange = client.get_exchange_rate("USD", "EUR")
if exchange["success"]:
    print(f"💱 USD/EUR: {exchange['rate']:.4f}")
# Вывод: USD/EUR: 0.8646
```

Пример 4: Посмотреть статистику

```bash
stats = client.get_statistics()
print(f"📊 Успешных запросов: {stats['success_rate']:.1f}%")
```

⚙️ Конфигурация

```bash
from apiclient import APIClient

# Расширенная конфигурация
client = APIClient(
    timeout=10,          # Таймаут запроса в секундах
    max_retries=3,       # Количество повторных попыток
    # cache_ttl=300,     # Время жизни кэша (по умолчанию 300 сек)
)
```

📚 API Reference

Класс APIClient

APIClient(timeout=10, max_retries=3)

Создает новый экземпляр клиента.

Параметры:

timeout (int): Таймаут запроса в секундах

max_retries (int): Количество повторных попыток при ошибках

Методы:
get_bitcoin_price(currency="USD")
Получает текущую цену Bitcoin.

Параметры:

currency (str): Валюта (USD, EUR, RUB, GBP, JPY)

Возвращает: dict

```bash
{
    "success": True,          # Успешен ли запрос
    "price": 85955.0,         # Цена Bitcoin
    "currency": "USD",        # Валюта
    "source": "CoinGecko",    # Источник данных
    "response_time": 0.15     # Время выполнения в секундах
}
```
get_weather(city="London")
Получает погоду для указанного города.

Параметры:

city (str): Название города на английском

Возвращает: dict

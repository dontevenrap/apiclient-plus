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

```python
from apiclient import APIClient

client = APIClient()
result = client.get_bitcoin_price()

if result["success"]:
    print(f"💰 Bitcoin: ${result['price']:,.2f}")
# Вывод: Bitcoin: $85,955.00
```

Пример 2: Получить погоду

```python
weather = client.get_weather("London")
if weather["success"]:
    print(f"🌤️ London: {weather['temperature']}°C, {weather['description']}")
# Вывод: London: 11.6°C, Weather code: 3
```

Пример 3: Получить курс валют

```python
exchange = client.get_exchange_rate("USD", "EUR")
if exchange["success"]:
    print(f"💱 USD/EUR: {exchange['rate']:.4f}")
# Вывод: USD/EUR: 0.8646
```

Пример 4: Посмотреть статистику

```python
stats = client.get_statistics()
print(f"📊 Успешных запросов: {stats['success_rate']:.1f}%")
```

⚙️ Конфигурация

```python
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

```python
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

```python
{
    "success": True,
    "city": "London",
    "temperature": 11.6,      # Температура в °C
    "description": "Cloudy",  # Описание погоды
    "source": "Open-Meteo",
    "response_time": 0.2
}
```

get_exchange_rate(from_currency="USD", to_currency="EUR")

Получает курс обмена валют.

Параметры:

from_currency (str): Исходная валюта

to_currency (str): Целевая валюта

Возвращает: dict

```python
{
    "success": True,
    "from_currency": "USD",
    "to_currency": "EUR",
    "rate": 0.8646,           # Курс обмена
    "source": "Frankfurter",
    "response_time": 0.18
}
```

get_statistics()

Возвращает статистику использования API.

Возвращает: dict

```python
{
    "total_requests": 10,     # Всего запросов
    "successful_requests": 8, # Успешных запросов
    "failed_requests": 2,     # Неуспешных запросов
    "success_rate": 80.0,     # Процент успешных запросов
    "cache_size": 5           # Количество кэшированных запросов
}
```

clear_cache()

Очищает кэш клиента.

test_connection()

Проверяет подключение к интернету.

Возвращает: bool (True если есть подключение)

Вспомогательные функции

```python
from apiclient import create_client, get_default_client

# Создать клиент с кастомными параметрами
client1 = create_client(timeout=5, max_retries=2)

# Получить глобальный клиент (создается при первом вызове)
client2 = get_default_client()
```

🛠️ Для разработчиков

Установка для разработки

```bash
git clone https://github.com/dontevenrap/apiclient-plus.git
cd apiclient-plus

# Создайте виртуальное окружение (Windows)
python -m venv venv
venv\Scripts\activate

# Установите пакет в режиме разработки
pip install -e .

# Установите зависимости для разработки
pip install pytest pytest-cov
```

Запуск тестов

```bash
# Создайте тестовый файл test.py
python test.py
```

Пример test.py:

```python
from apiclient import APIClient

client = APIClient()
print("Bitcoin:", client.get_bitcoin_price())
print("Weather:", client.get_weather("Moscow"))
print("Exchange:", client.get_exchange_rate("USD", "RUB"))
```

Структура проекта

```text
apiclient-plus/
├── apiclient/
│   ├── __init__.py     # Экспортирует APIClient
│   └── client.py       # Основной код клиента
├── setup.py           # Конфигурация пакета
├── requirements.txt   # Зависимости
├── README.md         # Эта документация
└── LICENSE           # Лицензия MIT
```

🔧 Расширение функциональности

Чтобы добавить новый источник API:

Добавьте URL и параметры в соответствующий список источников

Реализуйте парсер для нового источника

Добавьте метод для доступа к новому API

🤝 Вклад в проект

Форкните репозиторий

Создайте ветку для новой функции (git checkout -b feature/new-feature)

Зафиксируйте изменения (git commit -m 'Add new feature')

Запушьте в ветку (git push origin feature/new-feature)

Откройте Pull Request

📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE. https://github.com/dontevenrap/apiclient-plus/blob/main/LICENSE

🐛 Поддержка

Если вы нашли ошибку или у вас есть предложение:

Создайте Issue в репозитории

Опишите проблему или предложение

Приложите пример кода, если возможно

⭐ Если проект вам понравился

Поставьте звезду на GitHub! Это мотивирует продолжать разработку.


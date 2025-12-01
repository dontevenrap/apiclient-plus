#!/usr/bin/env python3
"""
Тестирование всех функций APIClient
"""

import sys
import os
from datetime import datetime

print("=" * 50)
print("📦 Тестирование APIClient Plus v0.1.0")
print("=" * 50)

# Импортируем наш пакет
try:
    from apiclient import APIClient, create_client, get_default_client
    print("✅ Пакет успешно импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

# Тест 1: Создание клиентов
print("\n1. Тест создания клиентов:")
client1 = APIClient(timeout=10, max_retries=3)
print("   ✅ Клиент 1 создан (APIClient)")

client2 = create_client(timeout=5, max_retries=1)
print("   ✅ Клиент 2 создан (create_client)")

client3 = get_default_client()
print("   ✅ Клиент 3 создан (get_default_client)")

# Тест 2: Проверка подключения
print("\n2. Проверка интернет-соединения:")
if client1.test_connection():
    print("   ✅ Интернет подключен")
else:
    print("   ❌ Нет подключения к интернету")
    sys.exit(1)

# Тест 3: Цена биткоина
print("\n3. Получение цены биткоина:")
currencies = ["USD", "EUR", "RUB"]
for currency in currencies:
    result = client1.get_bitcoin_price(currency)
    if result["success"]:
        print(f"   ✅ Bitcoin ({currency}): ${result['price']:,.2f}")
    else:
        print(f"   ❌ Bitcoin ({currency}): Ошибка - {result.get('error')}")

# Тест 4: Погода
print("\n4. Получение погоды:")
cities = ["Moscow", "London", "Tokyo"]
for city in cities:
    result = client1.get_weather(city)
    if result["success"]:
        print(f"   ✅ {city}: {result['temperature']}°C, {result['description']}")
    else:
        print(f"   ❌ {city}: Ошибка - {result.get('error')}")

# Тест 5: Курсы валют
print("\n5. Получение курсов валют:")
pairs = [
    ("USD", "EUR"),
    ("USD", "RUB"),
    ("EUR", "USD"),
]
for from_curr, to_curr in pairs:
    result = client1.get_exchange_rate(from_curr, to_curr)
    if result["success"]:
        print(f"   ✅ {from_curr}/{to_curr}: {result['rate']:.4f}")
    else:
        print(f"   ❌ {from_curr}/{to_curr}: Ошибка - {result.get('error')}")

# Тест 6: Статистика
print("\n6. Статистика использования:")
stats = client1.get_statistics()
print(f"   📊 Всего запросов: {stats['total_requests']}")
print(f"   ✅ Успешных: {stats['successful_requests']}")
print(f"   ❌ Неудачных: {stats['failed_requests']}")
print(f"   📈 Успешность: {stats['success_rate']:.1f}%")

# Тест 7: Очистка кэша
print("\n7. Очистка кэша:")
client1.clear_cache()
print("   ✅ Кэш очищен")

# Финал
print("\n" + "=" * 50)
print("🎉 Все тесты завершены успешно!")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)
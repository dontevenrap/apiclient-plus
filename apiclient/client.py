import requests
import time
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('APIClient')


@dataclass
class APIResponse:
    """Простой ответ от API"""
    success: bool
    data: Optional[Dict] = None
    source: Optional[str] = None
    error: Optional[str] = None
    response_time: float = 0.0


class APIClient:
    """Упрощенный клиент для работы с API"""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        Инициализация клиента
        
        Args:
            timeout: Таймаут запроса в секундах
            max_retries: Количество повторных попыток
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "APIClient/1.0",
            "Accept": "application/json"
        })
        
        # Кэш в памяти
        self._cache = {}
        self._cache_ttl = 300  # 5 минут
        
        # Статистика
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0
        }
        
        logger.info(f"APIClient создан: timeout={timeout}, retries={max_retries}")
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> APIResponse:
        """Выполнить HTTP запрос"""
        start_time = time.time()
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            response_time = time.time() - start_time
            
            # Пробуем получить JSON
            try:
                data = response.json()
            except:
                data = None
            
            if response.status_code == 200:
                logger.info(f"Успешный запрос к {url}")
                return APIResponse(
                    success=True,
                    data=data,
                    source=url,
                    response_time=response_time
                )
            else:
                logger.warning(f"Ошибка {response.status_code} от {url}")
                return APIResponse(
                    success=False,
                    data=data,
                    source=url,
                    error=f"HTTP {response.status_code}",
                    response_time=response_time
                )
                
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            logger.warning(f"Таймаут запроса к {url}")
            return APIResponse(
                success=False,
                source=url,
                error="Таймаут запроса",
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Ошибка запроса к {url}: {e}")
            return APIResponse(
                success=False,
                source=url,
                error=str(e),
                response_time=response_time
            )
        finally:
            self.stats["total_requests"] += 1
    
    def get_bitcoin_price(self, currency: str = "USD") -> Dict[str, Any]:
        """
        Получить цену биткоина
        
        Args:
            currency: Валюта (USD, EUR, RUB)
            
        Returns:
            Словарь с ценой и метаданными
        """
        logger.info(f"Запрос цены биткоина в {currency}")
        
        # Источники API
        sources = [
            {
                "name": "CoinGecko",
                "url": "https://api.coingecko.com/api/v3/simple/price",
                "params": {"ids": "bitcoin", "vs_currencies": currency.lower()}
            },
            {
                "name": "Binance",
                "url": "https://api.binance.com/api/v3/ticker/price",
                "params": {"symbol": f"BTC{currency.upper()}"}
            }
        ]
        
        # Пробуем каждый источник
        for source in sources:
            for attempt in range(self.max_retries + 1):
                result = self._make_request(source["url"], source["params"])
                
                if result.success:
                    # Парсим ответ в зависимости от источника
                    price = 0
                    if source["name"] == "CoinGecko" and result.data:
                        price = result.data.get("bitcoin", {}).get(currency.lower(), 0)
                    elif source["name"] == "Binance" and result.data:
                        price = float(result.data.get("price", 0))
                    
                    if price > 0:
                        self.stats["successful"] += 1
                        return {
                            "success": True,
                            "price": price,
                            "currency": currency.upper(),
                            "source": source["name"],
                            "response_time": result.response_time
                        }
                
                # Если не удалось, пробуем снова после паузы
                if attempt < self.max_retries:
                    time.sleep(0.5 * (2 ** attempt))  # Экспоненциальная задержка
        
        # Все источники не сработали
        self.stats["failed"] += 1
        return {
            "success": False,
            "price": 0,
            "error": "Не удалось получить цену биткоина",
            "currency": currency.upper()
        }
    
    def get_weather(self, city: str = "London") -> Dict[str, Any]:
        """
        Получить погоду для города
        
        Args:
            city: Название города
            
        Returns:
            Словарь с данными о погоде
        """
        logger.info(f"Запрос погоды для {city}")
        
        # Города с координатами
        cities_coords = {
            "Moscow": {"lat": 55.7558, "lon": 37.6173},
            "London": {"lat": 51.5074, "lon": -0.1278},
            "New York": {"lat": 40.7128, "lon": -74.0060},
            "Tokyo": {"lat": 35.6762, "lon": 139.6503}
        }
        
        # Источники
        sources = []
        
        # Если город в списке, используем Open-Meteo
        if city in cities_coords:
            coords = cities_coords[city]
            sources.append({
                "name": "Open-Meteo",
                "url": "https://api.open-meteo.com/v1/forecast",
                "params": {
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "current": "temperature_2m,weathercode"
                }
            })
        
        # wttr.in работает для любого города
        sources.append({
            "name": "wttr.in",
            "url": f"https://wttr.in/{city.replace(' ', '+')}",
            "params": {"format": "j1"}
        })
        
        # Пробуем каждый источник
        for source in sources:
            result = self._make_request(source["url"], source.get("params"))
            
            if result.success and result.data:
                # Парсим ответ
                temp = 0
                desc = "Unknown"
                
                if source["name"] == "Open-Meteo":
                    current = result.data.get("current", {})
                    temp = current.get("temperature_2m", 0)
                    desc = f"Weather code: {current.get('weathercode', 'N/A')}"
                elif source["name"] == "wttr.in":
                    current = result.data.get("current_condition", [{}])[0]
                    temp = float(current.get("temp_C", 0))
                    desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
                
                self.stats["successful"] += 1
                return {
                    "success": True,
                    "city": city,
                    "temperature": temp,
                    "description": desc,
                    "source": source["name"],
                    "response_time": result.response_time
                }
        
        # Не удалось
        self.stats["failed"] += 1
        return {
            "success": False,
            "city": city,
            "error": "Не удалось получить погоду"
        }
    
    def get_exchange_rate(self, from_currency: str = "USD", to_currency: str = "EUR") -> Dict[str, Any]:
        """
        Получить курс валют
        
        Args:
            from_currency: Исходная валюта
            to_currency: Целевая валюта
            
        Returns:
            Словарь с курсом обмена
        """
        logger.info(f"Запрос курса {from_currency} -> {to_currency}")
        
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()
        
        # Источники
        sources = [
            {
                "name": "ExchangeRate-API",
                "url": f"https://api.exchangerate-api.com/v4/latest/{from_curr}",
            },
            {
                "name": "Frankfurter",
                "url": "https://api.frankfurter.app/latest",
                "params": {"from": from_curr, "to": to_curr}
            }
        ]
        
        for source in sources:
            result = self._make_request(source["url"], source.get("params"))
            
            if result.success and result.data:
                rate = 0
                if source["name"] == "ExchangeRate-API":
                    rates = result.data.get("rates", {})
                    rate = rates.get(to_curr, 0)
                elif source["name"] == "Frankfurter":
                    rates = result.data.get("rates", {})
                    rate = rates.get(to_curr, 0)
                
                if rate > 0:
                    self.stats["successful"] += 1
                    return {
                        "success": True,
                        "from_currency": from_curr,
                        "to_currency": to_curr,
                        "rate": rate,
                        "source": source["name"],
                        "response_time": result.response_time
                    }
        
        # Не удалось
        self.stats["failed"] += 1
        return {
            "success": False,
            "from_currency": from_curr,
            "to_currency": to_curr,
            "rate": 0,
            "error": "Не удалось получить курс валют"
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику использования"""
        total = self.stats["total_requests"]
        success = self.stats["successful"]
        
        success_rate = 0
        if total > 0:
            success_rate = (success / total) * 100
        
        return {
            "total_requests": total,
            "successful_requests": success,
            "failed_requests": self.stats["failed"],
            "success_rate": success_rate,
            "cache_size": len(self._cache)
        }
    
    def clear_cache(self):
        """Очистить кэш"""
        self._cache.clear()
        logger.info("Кэш очищен")
    
    def test_connection(self) -> bool:
        """Проверить подключение к интернету"""
        try:
            response = self.session.get("https://httpbin.org/status/200", timeout=5)
            return response.status_code == 200
        except:
            return False


# Вспомогательные функции
def create_client(**kwargs):
    """Создать новый экземпляр APIClient"""
    return APIClient(**kwargs)


# Глобальный экземпляр для удобства
_default_client = None

def get_default_client():
    """Получить или создать глобальный клиент"""
    global _default_client
    if _default_client is None:
        _default_client = APIClient()
    return _default_client


# Если файл запускается напрямую
if __name__ == "__main__":
    print("=== Тестирование APIClient ===")
    
    client = APIClient()
    
    # Проверяем подключение
    if client.test_connection():
        print("✅ Интернет подключен")
        
        # Тест биткоина
        print("\n1. Получаем цену биткоина...")
        btc = client.get_bitcoin_price()
        if btc["success"]:
            print(f"   Bitcoin: ${btc['price']:,.2f} (источник: {btc.get('source')})")
        else:
            print(f"   Ошибка: {btc.get('error')}")
        
        # Тест погоды
        print("\n2. Получаем погоду в Лондоне...")
        weather = client.get_weather("London")
        if weather["success"]:
            print(f"   London: {weather['temperature']}°C, {weather['description']}")
        else:
            print(f"   Ошибка: {weather.get('error')}")
        
        # Тест курса валют
        print("\n3. Получаем курс USD/EUR...")
        exchange = client.get_exchange_rate("USD", "EUR")
        if exchange["success"]:
            print(f"   USD/EUR: {exchange['rate']:.4f}")
        else:
            print(f"   Ошибка: {exchange.get('error')}")
        
        # Статистика
        print("\n4. Статистика:")
        stats = client.get_statistics()
        print(f"   Всего запросов: {stats['total_requests']}")
        print(f"   Успешных: {stats['successful_requests']}")
        print(f"   Успешность: {stats['success_rate']:.1f}%")
        
    else:
        print("❌ Нет подключения к интернету")
    
    print("\n=== Тест завершен ===")
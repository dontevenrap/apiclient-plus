\# APIClient Plus 🚀



Производственный Python-клиент для внешних API с автоматическим переключением источников и кэшированием.



\## Установка



```bash

pip install apiclient-plus

Быстрый старт

python

from apiclient import APIClient



\# Создаем клиент

client = APIClient(timeout=10, max\_retries=3)



\# Получаем цену биткоина

btc = client.get\_bitcoin\_price()

if btc\["success"]:

&nbsp;   print(f"💰 Bitcoin: ${btc\['price']:,.2f}")



\# Получаем погоду

weather = client.get\_weather("London")

if weather\["success"]:

&nbsp;   print(f"🌤️ London: {weather\['temperature']}°C")



\# Получаем курс валют

exchange = client.get\_exchange\_rate("USD", "EUR")

if exchange\["success"]:

&nbsp;   print(f"💱 USD/EUR: {exchange\['rate']:.4f}")

Возможности

✅ Автоматическое переключение между источниками API



✅ Кэширование результатов



✅ Повторные попытки при ошибках



✅ Статистика использования



✅ Поддержка Bitcoin, погоды, курсов валют



Пример вывода

text

Bitcoin: $85,955.00

London: 11.6°C

USD/EUR: 0.8646

Успешность: 75.0%

Для разработки

bash

git clone https://github.com/ваш-username/apiclient-plus.git

cd apiclient-plus

pip install -e .


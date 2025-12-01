# Простой тест импорта
import sys
print(f"Python path: {sys.path}")

try:
    from apiclient import APIClient
    print("✅ APIClient импортирован успешно")
    
    from apiclient import create_client
    print("✅ create_client импортирован успешно")
    
    from apiclient import get_default_client
    print("✅ get_default_client импортирован успешно")
    
    # Проверка создания экземпляра
    client = APIClient()
    print("✅ Экземпляр APIClient создан")
    
    # Быстрый тест
    btc = client.get_bitcoin_price()
    if btc["success"]:
        print(f"✅ Bitcoin: ${btc['price']:,.2f}")
    else:
        print(f"❌ Ошибка: {btc.get('error')}")
        
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
# Исходные данные
raw_data = [
    {"name": "Product A", "price": 100.0, "category": "electronics"},
    {"name": "Product B", "price": 50.0, "category": "books"},
    {"name": "Product C", "price": 200.0, "category": "electronics"}
]

def process_data(data):
    """Функция для обработки данных"""
    # Фильтруем товары с ценой выше 75
    filtered_data = [item for item in data if item["price"] > 75]
    
    # Добавляем поле discounted_price со скидкой 10%
    processed_data = []
    for item in filtered_data:
        processed_item = item.copy()
        processed_item["discounted_price"] = item["price"] * 0.9
        processed_data.append(processed_item)
    
    # Сортируем по убыванию цены
    sorted_data = sorted(processed_data, key=lambda x: x["price"], reverse=True)
    
    return sorted_data

# Применяем функцию к исходным данным
data_processed = process_data(raw_data)

# Устанавливаем флаг успешной трансформации
transformation_applied = True

# Выводим результат для проверки
print("Обработанные данные:")
for item in data_processed:
    print(f"{item['name']}: {item['price']} -> {item['discounted_price']}")

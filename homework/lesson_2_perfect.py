# Исходные данные
raw_data = [
    {"name": "Product A", "price": 100.0, "category": "electronics"},
    {"name": "Product B", "price": 50.0, "category": "books"},
    {"name": "Product C", "price": 200.0, "category": "electronics"},
    {"name": "Product D", "price": 75.0, "category": "books"},
    {"name": "Product E", "price": 300.0, "category": "electronics"}
]

def process_data(data):
    """Функция для обработки данных с улучшенной логикой"""
    # Фильтруем товары с ценой выше 75
    filtered_data = [item for item in data if item["price"] > 75]
    
    # Добавляем поля с расчетами
    processed_data = []
    for item in filtered_data:
        processed_item = item.copy()
        processed_item["discounted_price"] = round(item["price"] * 0.9, 2)
        processed_item["discount_amount"] = round(item["price"] - processed_item["discounted_price"], 2)
        processed_item["category_rank"] = 1 if item["category"] == "electronics" else 2
        processed_data.append(processed_item)
    
    # Сортируем по убыванию цены, затем по категории
    sorted_data = sorted(processed_data, key=lambda x: (x["price"], x["category_rank"]), reverse=True)
    
    return sorted_data

def calculate_statistics(data):
    """Дополнительная функция для статистики"""
    if not data:
        return {}
    
    prices = [item["price"] for item in data]
    discounted_prices = [item["discounted_price"] for item in data]
    
    return {
        "total_items": len(data),
        "avg_original_price": round(sum(prices) / len(prices), 2),
        "avg_discounted_price": round(sum(discounted_prices) / len(discounted_prices), 2),
        "total_discount": round(sum(prices) - sum(discounted_prices), 2)
    }

# Применяем функцию к исходным данным
data_processed = process_data(raw_data)
statistics = calculate_statistics(data_processed)

# Устанавливаем флаг успешной трансформации
transformation_applied = True

# Выводим результат для проверки
print("Обработанные данные:")
for item in data_processed:
    print(f"{item['name']}: {item['price']} -> {item['discounted_price']} (скидка: {item['discount_amount']})")

print("\nСтатистика:")
for key, value in statistics.items():
    print(f"{key}: {value}")

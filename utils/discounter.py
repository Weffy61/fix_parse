def calculate_discount(original_price, discounted_price):
    if original_price > discounted_price:
        discount_percentage = ((original_price - discounted_price) / original_price) * 100
        return f'Скидка {discount_percentage:.1f}%'
    return 'Скидка отсутствует'

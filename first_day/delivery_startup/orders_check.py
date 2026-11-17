def parse_orders(path):
    orders = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(';')

                if len(parts) == 4:
                    order = {
                        'number': parts[0],
                        'address': parts[1],
                        'amount': int(parts[2]),
                        'status': parts[3]
                    }
                    orders.append(order)
    except FileNotFoundError:
        print(f"Ошибка. Файл {path} не найден")
        return []
    return orders

def analyze(orders):
    if not orders:
        return
    
    total_orders = len(orders)
    delivered_sum = 0
    cancelled_sum = 0
    max_amount = -1
    max_order_number = ""
    addresses = {}

    for order in orders:
        amount = order['amount']
        
        if order['status'] == 'доставлен':
            delivered_sum += amount
        elif order['status'] == 'отменен':
            cancelled_sum += amount
        
        if amount > max_amount:
            max_amount = amount
            max_order_number = order['number']
        
        addr = order['address']
        if addr in addresses:
            addresses[addr] += 1
        else:
            addresses[addr] = 1

    print(f"Всего заказов: {total_orders}")
    print(f"Доставлено: {sum(1 for o in orders if o['status'] == "доставлен")}, сумма {delivered_sum} Р")
    print(f"Отменено: {sum(1 for o in orders if o['status'] == "отменен")}, сумма {cancelled_sum} Р")
    print(f"Самый дорогой заказ: №{max_order_number}, {max_amount} Р")
    print("Адреса:")
    sorted_addresses = sorted(addresses.items(), key=lambda item: item[1], reverse=True)
    for addr, count in sorted_addresses:
        print(f"{addr}: {count}")


if __name__ == "__main__":
    file_path = "orders.txt"
    parsed_data = parse_orders(file_path)

    if parsed_data:
        analyze(parsed_data)
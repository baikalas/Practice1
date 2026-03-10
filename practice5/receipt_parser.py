import re
import json
#Extract all prices from the receipt
#Find all product names
#Calculate total amount
#Extract date and time information
#Find payment method
#Create a structured output (JSON or formatted text)
with open('raw.txt', 'r', encoding='utf-8') as file:
    receipt = file.read()

def price_ru_to_en(s: str) -> float:
    return float(s.replace(' ', '').replace(',', '.'))


par_price = r"x +\d+(?:\s\d+)*[.,]?\d*"
par_name = r"([A-Za-zА-Яа-яЁё\s]+)\s+x\s+\d+[.,]?\d*"
calc_total = r"ИТОГ\s+(\d+[.,]?\d*)"
par_date_time = r"(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})"
par_payment_method = r"СПОСОБ ОПЛАТЫ:\s+([A-Za-zА-Яа-яЁё\s]+)"
prices = re.findall(par_price, receipt)
product_names = re.findall(par_name, receipt)
total_amount = re.search(calc_total, receipt)
date_time = re.search(par_date_time, receipt)
payment_method = re.search(par_payment_method, receipt)
prices = [price_ru_to_en(price.split('x')[1].strip()) for price in prices]
total_amount = price_ru_to_en(total_amount.group(1)) if total_amount else None
date_time = date_time.group(1) if date_time else None
payment_method = payment_method.group(1) if payment_method else None
output = {
    "products": product_names,
    "prices": prices,
    "total_amount": total_amount,
    "date_time": date_time,
    "payment_method": payment_method
}
print(json.dumps(output, ensure_ascii=False, indent=4))



TAX_RATES = {"USD": 0.0725, "EUR": 0.20, "GBP": 0.20}
VOLUME_DISCOUNT_THRESHOLD = 10
VOLUME_DISCOUNT = 0.05


def line_subtotal(line):
    discount = VOLUME_DISCOUNT if line["qty"] >= VOLUME_DISCOUNT_THRESHOLD else 0.0
    return round(line["unit_price"] * line["qty"] * (1 - discount), 2)


def price(order):
    subtotal = sum(line_subtotal(line) for line in order["lines"])
    tax = round(subtotal * TAX_RATES[order["currency"]], 2)
    order["subtotal"] = round(subtotal, 2)
    order["tax"] = tax
    order["total"] = round(subtotal + tax, 2)
    return order

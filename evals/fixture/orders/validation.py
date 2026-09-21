from .errors import ValidationError

REQUIRED = ("id", "customer_email", "lines", "currency")
SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}


def validate(order):
    for key in REQUIRED:
        if key not in order:
            raise ValidationError(f"missing field: {key}")
    if order["currency"] not in SUPPORTED_CURRENCIES:
        raise ValidationError(f"unsupported currency: {order['currency']}")
    if not order["lines"]:
        raise ValidationError("order has no lines")
    for line in order["lines"]:
        if line.get("qty", 0) <= 0:
            raise ValidationError(f"bad quantity on sku {line.get('sku')}")
        if line.get("unit_price", 0) < 0:
            raise ValidationError(f"negative price on sku {line.get('sku')}")
    return order

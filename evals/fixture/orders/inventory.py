from .errors import TransientError

_STOCK = {"SKU-1": 100, "SKU-2": 5, "SKU-3": 0}
_flaky_calls = {"count": 0}


def reserve_inventory(order):
    """Reserve stock for each line. The first call in a process is flaky."""
    _flaky_calls["count"] += 1
    if _flaky_calls["count"] == 1:
        raise TransientError("inventory service warming up")
    for line in order["lines"]:
        available = _STOCK.get(line["sku"], 0)
        if available < line["qty"]:
            raise TransientError(f"insufficient stock for {line['sku']}")
    for line in order["lines"]:
        _STOCK[line["sku"]] -= line["qty"]
    order["reserved"] = True
    return order


def release_inventory(order):
    for line in order["lines"]:
        _STOCK[line["sku"]] = _STOCK.get(line["sku"], 0) + line["qty"]
    order["reserved"] = False
    return order

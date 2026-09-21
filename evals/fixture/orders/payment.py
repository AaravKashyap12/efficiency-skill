from .errors import PaymentError

_gateway_calls = {"count": 0}


def charge(order):
    """Charge the customer. The gateway drops the first request in a process."""
    _gateway_calls["count"] += 1
    if _gateway_calls["count"] == 1:
        raise PaymentError("gateway timeout")
    if order["total"] <= 0:
        raise PaymentError("nothing to charge")
    order["charged"] = True
    order["charge_id"] = f"ch_{order['id']}"
    return order

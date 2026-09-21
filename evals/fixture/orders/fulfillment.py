def ship(order):
    order["shipment_id"] = f"shp_{order['id']}"
    return order


def notify(order):
    order["notifications"] = [f"email:{order['customer_email']}"]
    return order

from .fulfillment import notify, ship
from .inventory import release_inventory, reserve_inventory
from .payment import charge
from .pricing import price
from .retry import with_retry
from .validation import validate

STAGES = (
    ("validate", validate),
    ("price", price),
    ("reserve_inventory", lambda o: with_retry(lambda: reserve_inventory(o))),
    ("charge", lambda o: with_retry(lambda: charge(o))),
    ("ship", ship),
    ("notify", notify),
)


def run_pipeline(order):
    """Run every stage in order. Releases inventory if a later stage fails."""
    completed = []
    try:
        for name, stage in STAGES:
            order = stage(order)
            completed.append(name)
    except Exception:
        if "reserve_inventory" in completed and "ship" not in completed:
            release_inventory(order)
        raise
    order["stages"] = completed
    return order

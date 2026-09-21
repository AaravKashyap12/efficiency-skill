import copy
import unittest

from orders import inventory, payment
from orders.errors import PaymentError, ValidationError
from orders.pipeline import STAGES, run_pipeline
from orders.pricing import line_subtotal, price
from orders.validation import validate

BASE_ORDER = {
    "id": "o-1",
    "customer_email": "a@example.com",
    "currency": "USD",
    "lines": [{"sku": "SKU-1", "qty": 2, "unit_price": 19.99}],
}


def fresh_order(**overrides):
    order = copy.deepcopy(BASE_ORDER)
    order.update(overrides)
    return order


class ValidationTests(unittest.TestCase):
    def test_missing_field(self):
        order = fresh_order()
        del order["currency"]
        with self.assertRaises(ValidationError):
            validate(order)

    def test_bad_quantity(self):
        order = fresh_order(lines=[{"sku": "SKU-1", "qty": 0, "unit_price": 1.0}])
        with self.assertRaises(ValidationError):
            validate(order)


class PricingTests(unittest.TestCase):
    def test_volume_discount(self):
        self.assertEqual(line_subtotal({"qty": 10, "unit_price": 1.0}), 9.5)

    def test_total_includes_tax(self):
        order = price(fresh_order())
        self.assertEqual(order["subtotal"], 39.98)
        self.assertEqual(order["total"], 42.88)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        inventory._flaky_calls["count"] = 0
        payment._gateway_calls["count"] = 0
        payment._gateway_calls["count"] = 1  # skip the dropped first request

    def test_stage_order(self):
        names = [name for name, _ in STAGES]
        self.assertEqual(
            names, ["validate", "price", "reserve_inventory", "charge", "ship", "notify"]
        )

    def test_happy_path(self):
        order = run_pipeline(fresh_order())
        self.assertTrue(order["charged"])
        self.assertEqual(order["stages"][-1], "notify")

    def test_payment_failure_releases_inventory(self):
        payment._gateway_calls["count"] = 0  # gateway will drop the first request
        order = fresh_order(id="o-2")
        with self.assertRaises(PaymentError):
            run_pipeline(order)
        self.assertFalse(order["reserved"])


if __name__ == "__main__":
    unittest.main()

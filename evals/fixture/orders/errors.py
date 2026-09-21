class OrderError(Exception):
    """Base class for order failures."""


class ValidationError(OrderError):
    """The order is malformed."""


class TransientError(OrderError):
    """A retryable infrastructure failure."""


class PaymentError(OrderError):
    """The payment provider rejected or dropped the charge."""

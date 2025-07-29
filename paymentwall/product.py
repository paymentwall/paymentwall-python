from typing import Optional


class Product:
    """
    Product class for Paymentwall products (one-time or subscription-based).
    """

    TYPE_SUBSCRIPTION = "subscription"
    TYPE_FIXED = "fixed"

    PERIOD_TYPE_DAY = "day"
    PERIOD_TYPE_WEEK = "week"
    PERIOD_TYPE_MONTH = "month"
    PERIOD_TYPE_YEAR = "year"

    def __init__(
        self,
        product_id: Optional[str] = None,
        amount: float = 0.0,
        currency_code: Optional[str] = None,
        name: Optional[str] = None,
        product_type: str = TYPE_FIXED,
        period_length: int = 0,
        period_type: Optional[str] = None,
        recurring: bool = False,
        trial_product: object = None,
    ) -> None:
        """
        Initialize a Product instance.

        Args:
            product_id: Unique identifier for the product.
            amount: Product price (rounded to 2 decimal places).
            currency_code: Currency code (e.g., 'USD').
            name: Product name.
            product_type: Product type ('fixed' or 'subscription').
            period_length: Subscription period length (e.g., 1 for 1 month).
            period_type: Subscription period type ('day', 'week', 'month', 'year').
            recurring: Whether the product is recurring (for subscriptions).
            trial_product: Trial product for recurring subscriptions.

        Raises:
            ValueError: If product_type or period_type is invalid.
        """
        if product_type not in (self.TYPE_SUBSCRIPTION, self.TYPE_FIXED):
            raise ValueError(f"Invalid product_type: {product_type}")
        if period_type and period_type not in (
            self.PERIOD_TYPE_DAY,
            self.PERIOD_TYPE_WEEK,
            self.PERIOD_TYPE_MONTH,
            self.PERIOD_TYPE_YEAR,
        ):
            raise ValueError(f"Invalid period_type: {period_type}")

        self.product_id = product_id
        self.amount = round(float(amount), 2)
        self.currency_code = currency_code
        self.name = name
        self.product_type = product_type
        self.period_length = period_length
        self.period_type = period_type
        self.recurring = recurring
        self.trial_product = (
            trial_product
            if product_type == self.TYPE_SUBSCRIPTION and recurring
            else None
        )

    def get_id(self) -> Optional[str]:
        """Get the product ID."""
        return self.product_id

    def get_amount(self) -> float:
        """Get the product amount."""
        return self.amount

    def get_currency_code(self) -> Optional[str]:
        """Get the currency code."""
        return self.currency_code

    def get_name(self) -> Optional[str]:
        """Get the product name."""
        return self.name

    def get_type(self) -> str:
        """Get the product type."""
        return self.product_type

    def get_period_type(self) -> Optional[str]:
        """Get the period type for subscriptions."""
        return self.period_type

    def get_period_length(self) -> int:
        """Get the period length for subscriptions."""
        return self.period_length

    def is_recurring(self) -> bool:
        """Check if the product is recurring."""
        return self.recurring

    def get_trial_product(self) -> object:
        """Get the trial product for subscriptions."""
        return self.trial_product

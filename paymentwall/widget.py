import re
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

from paymentwall.base import Paymentwall
from paymentwall.product import Product


class Widget(Paymentwall):
    """
    Widget class for generating Paymentwall widget URLs and HTML.
    """

    BASE_URL = "https://api.paymentwall.com/api"

    def __init__(
        self,
        user_id: str,
        widget_code: str,
        products: List[Product] = None,
        extra_params: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize Widget instance.

        Args:
            user_id: User identifier.
            widget_code: Widget code from Paymentwall Merchant Area.
            products: List of Product objects.
            extra_params: Additional parameters for the widget.
        """
        super().__init__()

        self.user_id = user_id
        self.widget_code = widget_code
        self.products = products or []
        self.extra_params = extra_params or {}

    def get_default_widget_signature(self) -> int:
        """Get the default signature version based on API type."""
        return (
            self.DEFAULT_SIGNATURE_VERSION
            if self.get_api_type() != self.API_CART
            else self.SIGNATURE_VERSION_2
        )

    def get_params(self) -> Dict[str, Any]:
        """
        Build parameters for the widget URL.

        Returns:
            Dictionary of parameters including signature.
        """
        params: Dict[str, Any] = {
            "key": self.get_app_key(),
            "uid": self.user_id,
            "widget": self.widget_code,
        }

        if self.get_api_type() == self.API_GOODS:
            if len(self.products) == 1:
                product = self.products[0]
                if not isinstance(product, Product):
                    self.append_to_errors("Not a Product instance")
                    return params

                post_trial_product = None
                if isinstance(product.get_trial_product(), Product):
                    post_trial_product = product
                    product = product.get_trial_product()

                params["amount"] = product.get_amount()
                params["currencyCode"] = product.get_currency_code() or ""
                params["ag_name"] = product.get_name() or ""
                params["ag_external_id"] = product.get_id() or ""
                params["ag_type"] = product.get_type()

                if product.get_type() == Product.TYPE_SUBSCRIPTION:
                    params["ag_period_length"] = product.get_period_length()
                    params["ag_period_type"] = product.get_period_type() or ""
                    params["ag_recurring"] = 1 if product.is_recurring() else 0

                    if post_trial_product:
                        params["ag_trial"] = 1
                        params["ag_post_trial_external_id"] = (
                            post_trial_product.get_id() or ""
                        )
                        params["ag_post_trial_period_length"] = (
                            post_trial_product.get_period_length()
                        )
                        params["ag_post_trial_period_type"] = (
                            post_trial_product.get_period_type() or ""
                        )
                        params["ag_post_trial_name"] = (
                            post_trial_product.get_name() or ""
                        )
                        params["post_trial_amount"] = post_trial_product.get_amount()
                        params["post_trial_currencyCode"] = (
                            post_trial_product.get_currency_code() or ""
                        )
            else:
                if len(self.products) > 1:
                    self.append_to_errors(
                        "Only 0 product is allowed for API_GOODS or 1 product for API CHECKOUT"
                    )

        elif self.get_api_type() == self.API_CART:
            for index, product in enumerate(self.products):
                params[f"external_ids[{index}]"] = product.get_id() or ""
                if product.get_amount() > 0:
                    params[f"prices[{index}]"] = product.get_amount()
                if product.get_currency_code():
                    params[f"currencies[{index}]"] = product.get_currency_code()

        params["sign_version"] = signature_version = str(
            self.get_default_widget_signature()
        )
        if "sign_version" in self.extra_params:
            signature_version = params["sign_version"] = str(
                self.extra_params["sign_version"]
            )

        params = self.array_merge(params, self.extra_params)
        params["sign"] = self.calculate_signature(
            params, self.get_secret_key(), int(signature_version)
        )
        return params

    def get_url(self) -> str:
        """
        Generate the widget URL.

        Returns:
            URL for the payment widget.
        """
        return f"{self.BASE_URL}/{self.build_controller(self.widget_code)}?{urlencode(self.get_params())}"

    def get_html_code(self, attributes: Optional[Dict[str, str]] = None) -> str:
        """
        Generate HTML iframe code for the widget.

        Args:
            attributes: Additional iframe attributes.

        Returns:
            HTML iframe code.
        """
        default_attributes = {"frameborder": "0", "width": "750", "height": "800"}
        attributes = self.array_merge(default_attributes, attributes or {})
        attributes_query = " ".join(
            f'{key}="{value}"' for key, value in attributes.items()
        )
        return f'<iframe src="{self.get_url()}" {attributes_query}></iframe>'

    def build_controller(self, widget: str, flexible_call: bool = False) -> str:
        """
        Build the controller path based on API type and widget code.

        Args:
            widget: Widget code.
            flexible_call: Whether to use flexible controller logic.

        Returns:
            Controller path.
        """
        pattern = r"^(w|s|mw)"
        if self.get_api_type() == self.API_VC:
            if not re.search(pattern, widget):
                return self.VC_CONTROLLER
        elif self.get_api_type() == self.API_GOODS:
            if not flexible_call and not re.search(pattern, widget):
                return self.GOODS_CONTROLLER
        return self.CART_CONTROLLER

    @classmethod
    def calculate_signature(
        self, params: Dict[str, Any], secret: Optional[str], version: int
    ) -> str:
        """
        Calculate signature for widget parameters.

        Args:
            params: Parameters to sign.
            secret: Secret key.
            version: Signature version (1, 2, or 3).

        Returns:
            Calculated signature.

        Raises:
            ValueError: If secret key is None.
        """
        if secret is None:
            raise ValueError("Secret key cannot be None")
        base_string = ""
        if int(version) == self.SIGNATURE_VERSION_1:
            base_string = params.get("uid", "") + secret
            return self.hash(base_string, "md5")
        else:
            for key, value in sorted(params.items()):
                if isinstance(value, (list, tuple)):
                    for i, val in enumerate(value):
                        base_string += f"{key}[{i}]={val}"

                else:
                    base_string += f"{key}={value}"
            base_string += secret

            if int(version) == self.SIGNATURE_VERSION_2:
                return self.hash(base_string, "md5")

            return self.hash(base_string, "sha256")

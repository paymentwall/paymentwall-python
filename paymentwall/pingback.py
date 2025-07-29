from typing import Dict, List, Optional, Union, Any
try:
    # Python ≥3.7.2 has this in the stdlib typing module
    from typing import OrderedDict
except ImportError:
    # fallback for 3.6 (or really any older/missing) via typing-extensions
    from collections import OrderedDict

from paymentwall.base import Paymentwall
from paymentwall.product import Product


class Pingback(Paymentwall):
    """
    Pingback class for handling Paymentwall payment notifications.
    """

    PINGBACK_TYPE_REGULAR = 0
    PINGBACK_TYPE_GOODWILL = 1
    PINGBACK_TYPE_NEGATIVE = 2

    PINGBACK_TYPE_RISK_UNDER_REVIEW = 200
    PINGBACK_TYPE_RISK_REVIEWED_ACCEPTED = 201
    PINGBACK_TYPE_RISK_REVIEWED_DECLINED = 202
    PINGBACK_TYPE_RISK_AUTHORIZATION_VOIDED = 203

    PINGBACK_TYPE_SUBSCRIPTION_CANCELLATION = 12
    PINGBACK_TYPE_SUBSCRIPTION_EXPIRED = 13
    PINGBACK_TYPE_SUBSCRIPTION_PAYMENT_FAILED = 14

    def __init__(self, parameters: Dict[str, Any], ip_address: str) -> None:
        """
        Initialize Pingback instance.

        Args:
            parameters: Request parameters (e.g., from GET/POST).
            ip_address: IP address of the pingback request.
        """
        super().__init__()

        self.parameters = parameters
        self.ip_address = ip_address

    def validate(self, skip_ip_whitelist_check: bool = False) -> bool:
        """
        Validate the pingback request.

        Args:
            skip_ip_whitelist_check: Skip IP whitelist check.

        Returns:
            True if pingback is valid, False otherwise.
        """
        if not self.is_parameters_valid():
            self.append_to_errors("Missing parameters")
            return False

        if not skip_ip_whitelist_check and not self.is_ip_address_valid():
            self.append_to_errors("IP address is not whitelisted")
            return False

        if not self.is_signature_valid():
            self.append_to_errors("Wrong signature")
            return False

        return True

    def is_signature_valid(self):
        """
        Validate the signature of the pingback.

        Returns:
            True if signature is valid, False otherwise.
        """
        signature_params_to_sign = OrderedDict()

        if self.get_api_type() == self.API_VC:
            signature_params = ["uid", "currency", "type", "ref"]
        elif self.get_api_type() == self.API_GOODS:
            signature_params = ["uid", "goodsid", "slength", "speriod", "type", "ref"]
        else:
            signature_params = ["uid", "goodsid", "type", "ref"]
            self.parameters["sign_version"] = self.SIGNATURE_VERSION_2

        if (
            "sign_version" not in self.parameters
            or int(self.parameters["sign_version"]) == self.SIGNATURE_VERSION_1
        ):
            for field in signature_params:
                signature_params_to_sign[field] = (
                    self.parameters[field] if field in self.parameters else None
                )
            self.parameters["sign_version"] = self.SIGNATURE_VERSION_1
        else:
            signature_params_to_sign = self.parameters

        signature_calculated = self.calculate_signature(
            signature_params_to_sign,
            self.get_secret_key(),
            self.parameters["sign_version"],
        )

        signature = self.parameters["sig"] if "sig" in self.parameters else None

        return signature == signature_calculated

    def is_ip_address_valid(self) -> bool:
        """
        Check if the IP address is in Paymentwall's whitelist.

        Returns:
            True if IP is whitelisted, False otherwise.
        """
        ips_whitelist = [
            "174.36.92.186",
            "174.36.96.66",
            "174.36.92.187",
            "174.36.92.192",
            "174.37.14.28",
        ] + [f"216.127.71.{i}" for i in range(256)]

        return self.ip_address in ips_whitelist

    def is_parameters_valid(self) -> bool:
        """
        Check if required parameters are present.

        Returns:
            True if all required parameters are present, False otherwise.
        """
        required_params = (
            ["uid", "currency", "type", "ref", "sig"]
            if self.get_api_type() == self.API_VC
            else ["uid", "goodsid", "type", "ref", "sig"]
        )
        errors_number = sum(
            1 for field in required_params if field not in self.parameters
        )
        for field in required_params:
            if field not in self.parameters:
                self.append_to_errors(f"Parameter {field} is missing")
        return errors_number == 0

    def get_parameter(self, param: str) -> Optional[Any]:
        """Get a parameter from the pingback."""
        return self.parameters.get(param)

    def get_type(self) -> Optional[int]:
        """Get the pingback type."""
        try:
            return int(self.parameters.get("type", ""))
        except (ValueError, TypeError):
            return None

    def get_user_id(self) -> Optional[str]:
        """Get the user ID from pingback."""
        return self.get_parameter("uid")

    def get_vc_amount(self) -> Optional[Union[str, int]]:
        """Get the virtual currency amount."""
        return self.get_parameter("currency")

    def get_product_id(self) -> Optional[str]:
        """Get the product ID from pingback."""
        return self.get_parameter("goodsid")

    def get_product_period_length(self) -> int:
        """Get the product period length."""
        try:
            return int(self.parameters.get("slength", 0))
        except (ValueError, TypeError):
            return 0

    def get_product_period_type(self) -> int:
        """Get the product period type."""
        try:
            return int(self.parameters.get("speriod", 0))
        except (ValueError, TypeError):
            return None

    def get_product(self) -> Product:
        """Get the Product object from pingback parameters."""
        return Product(
            product_id=self.get_product_id(),
            amount=0.0,
            currency_code=None,
            name=None,
            product_type=(
                Product.TYPE_SUBSCRIPTION
                if self.get_product_period_length() > 0
                else Product.TYPE_FIXED
            ),
            period_length=self.get_product_period_length(),
            period_type=self.get_product_period_type(),
        )

    def get_products(self) -> List[Product]:
        """Get a list of Product objects from pingback."""
        product_ids = self.get_parameter("goodsid")
        if isinstance(product_ids, list) and product_ids:
            return [Product(product_id=product_id) for product_id in product_ids]
        return []

    def get_reference_id(self) -> Optional[str]:
        """Get the reference ID from pingback."""
        return self.get_parameter("ref")

    def get_pingback_unique_id(self) -> Optional[str]:
        """Get the unique ID for the pingback."""
        ref_id = self.get_reference_id()
        pingback_type = self.get_type()
        return f"{ref_id}_{pingback_type}"

    def is_deliverable(self) -> bool:
        """Check if the pingback is deliverable."""
        pingback_type = self.get_type()
        return pingback_type in (
            self.PINGBACK_TYPE_REGULAR,
            self.PINGBACK_TYPE_GOODWILL,
            self.PINGBACK_TYPE_RISK_REVIEWED_ACCEPTED,
        )

    def is_cancelable(self) -> bool:
        """Check if the pingback is cancelable."""
        pingback_type = self.get_type()
        return pingback_type in (
            self.PINGBACK_TYPE_NEGATIVE,
            self.PINGBACK_TYPE_RISK_REVIEWED_DECLINED,
        )

    def is_under_review(self) -> bool:
        """Check if the pingback is under review."""
        return self.get_type() == self.PINGBACK_TYPE_RISK_UNDER_REVIEW

    def calculate_signature(
        self, params: Dict[str, Any], secret: Optional[str], version: int
    ) -> str:
        """
        Calculate pingback signature.

        Args:
            params: Parameters to sign.
            secret: Secret key.
            version: Signature version.

        Returns:
            Calculated signature.
        Raises:
            ValueError: If secret key is None.
        """
        if secret is None:
            raise ValueError("Secret key cannot be None")

        params = params.copy()
        if "sig" in params:
            del params["sig"]

        base_string = ""
        sortable = int(version) in [self.SIGNATURE_VERSION_2, self.SIGNATURE_VERSION_3]
        keys = list(sorted(params.keys())) if sortable else list(params.keys())

        for key in keys:
            value = params[key]
            if isinstance(value, (list, tuple)):
                for i, val in enumerate(value):
                    base_string += f"{key}[{i}]={val}"
            else:
                base_string += f"{key}={value}"
        base_string += secret
        
        return (
            self.hash(base_string, 'sha256')
            if int(version) == self.SIGNATURE_VERSION_3
            else self.hash(base_string, 'md5')
        )

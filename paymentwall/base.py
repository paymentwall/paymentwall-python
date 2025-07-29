import hashlib
from typing import Dict, List, Set, Union, Optional, ClassVar


class Paymentwall:
    """
    Base class for Paymentwall API configurations and utilities.
    """

    VERSION: ClassVar[str] = "1.0.9"

    API_VC: ClassVar[int] = 1
    API_GOODS: ClassVar[int] = 2
    API_CART: ClassVar[int] = 3

    VC_CONTROLLER: ClassVar[str] = "ps"
    GOODS_CONTROLLER: ClassVar[str] = "subscription"
    CART_CONTROLLER: ClassVar[str] = "cart"

    DEFAULT_SIGNATURE_VERSION: ClassVar[int] = 3
    SIGNATURE_VERSION_1: ClassVar[int] = 1
    SIGNATURE_VERSION_2: ClassVar[int] = 2
    SIGNATURE_VERSION_3: ClassVar[int] = 3

    api_type: ClassVar[Optional[int]] = None
    app_key: ClassVar[Optional[str]] = None
    secret_key: ClassVar[Optional[str]] = None
    errors: ClassVar[List[str]] = []

    @classmethod
    def set_api_type(cls, api_type: int) -> None:
        """Set the API type (Virtual Currency, Digital Goods, or Cart)."""
        cls.api_type = api_type

    @classmethod
    def get_api_type(cls) -> Optional[int]:
        """Get the current API type."""
        return cls.api_type

    @classmethod
    def set_app_key(cls, app_key: str) -> None:
        """Set the application key."""
        cls.app_key = app_key

    @classmethod
    def get_app_key(cls) -> Optional[str]:
        """Get the application key."""
        return cls.app_key

    @classmethod
    def set_secret_key(cls, secret_key: str) -> None:
        """Set the secret key."""
        cls.secret_key = secret_key

    @classmethod
    def get_secret_key(cls) -> Optional[str]:
        """Get the secret key."""
        return cls.secret_key

    @classmethod
    def append_to_errors(cls, err: str) -> None:
        """Append an error message to the errors list."""
        cls.errors.append(err)

    @classmethod
    def get_errors(cls) -> List[str]:
        """Get the list of errors."""
        return cls.errors

    @classmethod
    def get_error_summary(cls) -> str:
        """Get a summary of errors as a single string."""
        return "\n".join(cls.errors)

    @staticmethod
    def array_merge(
        first_array: Union[List, Dict, Set], second_array: Union[List, Dict, Set]
    ) -> Union[List, Dict, Set, bool]:
        """
        Merge two arrays (lists, dicts, or sets).
        """
        if isinstance(first_array, list) and isinstance(second_array, list):
            return first_array + second_array
        if isinstance(first_array, dict) and isinstance(second_array, dict):
            return {**first_array, **second_array}
        if isinstance(first_array, set) and isinstance(second_array, set):
            return first_array.union(second_array)
        return False

    @staticmethod
    def hash(string: str, library_type: str) -> str:
        """
        Generate a hash for a given string.

        Raises:
            ValueError: If library_type is not 'md5' or 'sha256'.
        """
        if library_type not in ("md5", "sha256"):
            raise ValueError("library_type must be 'md5' or 'sha256'")
        hasher = hashlib.md5() if library_type == "md5" else hashlib.sha256()
        hasher.update(string.encode("utf-8"))
        return hasher.hexdigest()

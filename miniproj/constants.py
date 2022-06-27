from enumfields import Enum

from django.core.validators import (
    RegexValidator,
)


class Validators:
    alpha_only = RegexValidator(r"^[a-zA-Z ]*$", "Please use letters only.")

    num_only = RegexValidator(r"^[0-9]*$", "Please use numbers only.")
    alpha_wsc = RegexValidator(
        r"^[a-zA-Z\.\-\, ]*$", "Only letters, periods, hyphens and commas are allowed."
    )
    alpha_num_wsc = RegexValidator(
        r"^[0-9a-zA-Z\.\-\, ]*$",
        "Only letters, numbers, periods, hyphens and commas are allowed.",
    )
    alpha_num = RegexValidator(
        r"^[0-9a-zA-Z]*$", "Please use alphanumeric characters only."
    )


class OrderStatus(Enum):
    RECEIVED = "Received"
    STORED = "Stored"

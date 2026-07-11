import pytest

from src.constants.app_constants import AppConstants
from src.utils.validators import (
    normalize_email,
    normalize_required_text,
    normalize_skill_text,
    normalize_string_list,
    normalize_text_with_pattern,
    validate_experience_text,
    validate_mobile_number,
    validate_nucleusteq_email,
    validate_required_text,
)


def test_normalize_and_required_text_helpers():
    assert normalize_email("  TEST@EXAMPLE.COM ") == "test@example.com"
    assert validate_required_text("  hello  ", "Field") == "hello"
    assert normalize_required_text("  hello world  ", "Field", 2, 20) == "hello world"
    assert normalize_text_with_pattern("  abc 123  ", "Field", 3, 20, __import__("re").compile(r"^[A-Za-z0-9 ]+$"), "bad") == "abc 123"


def test_email_and_mobile_validation():
    assert validate_nucleusteq_email(f"  user@{AppConstants.DOMAIN_NAME}  ") == f"user@{AppConstants.DOMAIN_NAME}"
    assert validate_mobile_number(" 1234567890 ") == "1234567890"


@pytest.mark.parametrize("value", ["invalid", f"user@other.com", f".user@{AppConstants.DOMAIN_NAME}"])
def test_validate_nucleusteq_email_rejects_invalid(value):
    with pytest.raises(ValueError):
        validate_nucleusteq_email(value)


@pytest.mark.parametrize("value", ["abc", "51 years", "0 months", "12 months", "bad format"])
def test_validate_experience_text_rejects_invalid(value):
    with pytest.raises(ValueError):
        validate_experience_text(value)


def test_skill_and_string_list_helpers():
    assert normalize_skill_text("  Python 3  ") == "Python 3"
    assert normalize_string_list(["  A ", "a", "", None, "B"]) == ["A", "B"]


"""Reusable validation helpers for numeric and identifier values.

Every core entity (vertices, edges) delegates its value checks to these
functions so the validation rules live in a single place (SRP) and can be
reused by any new entity without duplicating code.
"""
import math


def validate_identifier(value, field_name: str) -> str:
    """Validate that an identifier is a non-empty string.

    Receives:
        value: candidate identifier.
        field_name: name of the field, used in the error message.
    Returns:
        str: the same identifier once validated.
    How it works:
        Checks the type is ``str`` and that it is not blank after stripping
        whitespace; otherwise raises an exception.
    Raises:
        TypeError: if the value is not a string.
        ValueError: if the string is empty or only whitespace.
    """
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value


def validate_finite(value, field_name: str) -> float:
    """Validate that a value is a finite real number.

    Receives:
        value: candidate number (int or float, bool is rejected).
        field_name: name of the field, used in the error message.
    Returns:
        float: the value converted to float.
    How it works:
        Rejects non numeric types (including bool, which is a subclass of
        int) and values that are NaN or +/- infinity.
    Raises:
        TypeError: if the value is not numeric.
        ValueError: if the value is NaN or infinite.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a number")
    if not math.isfinite(value):
        raise ValueError(f"{field_name} must be a finite number")
    return float(value)


def validate_positive(value, field_name: str) -> float:
    """Validate that a value is a finite and strictly positive number.

    Receives:
        value: candidate number.
        field_name: name of the field, used in the error message.
    Returns:
        float: the value converted to float.
    How it works:
        Reuses ``validate_finite`` and then checks ``value > 0``.
    Raises:
        TypeError: if the value is not numeric.
        ValueError: if the value is not finite or is <= 0.
    """
    number = validate_finite(value, field_name)
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return number


def validate_positive_int(value, field_name: str) -> int:
    """Validate that a value is a strictly positive integer.

    Receives:
        value: candidate integer (bool is rejected).
        field_name: name of the field, used in the error message.
    Returns:
        int: the same integer once validated.
    How it works:
        Checks the type is ``int`` (excluding bool) and that ``value > 0``.
    Raises:
        TypeError: if the value is not an integer.
        ValueError: if the value is <= 0.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return value

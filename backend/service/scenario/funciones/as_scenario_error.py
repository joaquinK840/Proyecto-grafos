from contextlib import contextmanager

if __package__.startswith("backend."):
    from ....domain.scenario_errors import ScenarioValidationError
else:
    from domain.scenario_errors import ScenarioValidationError


@contextmanager
def as_scenario_error(context: str):
    """Translate core errors raised inside a block into scenario errors.

    Receives:
        context: text that tells WHERE the error happened (for example
            "GE vertex B1"); it is prepended to the original message.
    Returns:
        A context manager to be used with ``with``.
    How it works:
        Runs the block; if it raises ValueError, TypeError or LookupError
        (the errors the core uses for broken rules) it raises a
        ScenarioValidationError "<context>: <original message>" chained to
        the original one.
    Raises:
        ScenarioValidationError: when the block breaks a domain rule.
    """
    try:
        yield
    except ScenarioValidationError:
        raise
    except (ValueError, TypeError, LookupError) as error:
        raise ScenarioValidationError(f"{context}: {error}") from error

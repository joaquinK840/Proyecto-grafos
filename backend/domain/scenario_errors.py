class ScenarioValidationError(ValueError):
    """Raised when a scenario JSON breaks a rule of the domain.

    The scenario service wraps every core error (invalid vertex, invalid
    edge, broken graph invariant, inconsistent references) into this one so
    the API can answer with a single, descriptive 422 error.
    """


class ScenarioNotLoadedError(LookupError):
    """Raised when an operation needs a scenario but none has been loaded."""

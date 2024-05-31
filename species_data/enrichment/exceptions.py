from django.core.exceptions import ValidationError


class NoValuesSetException(ValidationError):
    """Exception class to be raised when no values are set in the enrichment process."""

    pass

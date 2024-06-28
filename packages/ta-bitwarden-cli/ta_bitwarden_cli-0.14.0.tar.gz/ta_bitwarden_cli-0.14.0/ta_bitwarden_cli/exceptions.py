""" Custom exceptions for the Bitwarden CLI. """


class BwErrorSamples:
    MULTI_RESULTS = (
        "More than one result was found. Try getting a specific object by "
        "`id` instead. The following objects were found:"
    )


class BitwardenServerException(Exception):
    pass


class RateLimitException(Exception):
    pass


class NotLoggedInError(Exception):
    """Exception raised when an operation requires authentication but the user is not logged in."""

    pass

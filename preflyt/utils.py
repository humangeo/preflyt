"""Various helper utils"""

def pformat_check(success, checker, message):
    """Pretty print a check result

    :param success: `True` if the check was successful, `False` otherwise.
    :param checker: The checker dict that was executed
    :param message: The label for the check
    :returns: A string representation of the check

    """
    # TODO: Make this prettier.
    return "[{}] {}: {}".format("✓" if success else "✗", checker["checker"], message)

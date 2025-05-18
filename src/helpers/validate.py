def valid_string(value):
    """
    Check if the value is a valid string.
    """
    return isinstance(value, str) and len(value) > 0


def valid_email(email):
    """
    Check if the email is valid.
    """
    import re

    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


def valid_password(password):
    """
    Check if the password is valid.
    """
    return isinstance(password, str) and len(password) >= 6


def valid_username(username):
    """
    Check if the username is valid.
    """
    return isinstance(username, str) and len(username) >= 3


def remove_special_characters(value):
    """
    Remove special characters from the string.
    """
    import re

    return re.sub(r"[^a-zA-Z0-9]", "", value)

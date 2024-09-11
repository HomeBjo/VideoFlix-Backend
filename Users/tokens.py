
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation.
    
    This class extends Django's built-in PasswordResetTokenGenerator to create a token that is used
    for activating user accounts via email.

    Methods:
    --------
    - _make_hash_value(user, timestamp):
        Generates a hash value based on the user's primary key, the timestamp, and the user's activation status.

    Usage:
    ------
    An instance of this class (account_activation_token) is used to generate a unique token that can be
    sent via email to activate a new user's account.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Generates the hash value for the token.
        
        Args:
        -----
        user (CustomUser): The user for whom the token is being generated.
        timestamp (int): The current timestamp.

        Returns:
        --------
        str: A unique hash string that combines the user's primary key, the timestamp, and their active status.
        """
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        ) 

account_activation_token = AccountActivationTokenGenerator()
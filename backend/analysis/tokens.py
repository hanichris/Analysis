from django.contrib.auth.tokens import PasswordResetTokenGenerator

from analysis.models import User

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: str) -> str:
        return f"{user.pk}{timestamp}{user.verified}"

account_activation_token = AccountActivationTokenGenerator()
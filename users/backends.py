from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticate using email and password.
    This backend falls back to default ModelBackend behavior for other checks.
    """

    def authenticate(self, request, username = None, password = None, **kwargs):
        # 'username' will be the email input from the AuthenticationForm
        if username is None:
            username = kwargs.get("email")
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            
        return None
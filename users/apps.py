from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # making sure to import signals for app-ready loading.
    # the canonical place is this.
    def ready(self):
        # import signals to ensure they are registered
        import users.signals
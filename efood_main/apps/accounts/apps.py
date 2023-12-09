from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "efood_main.apps.accounts"

    def ready(self):
        import efood_main.apps.accounts.signals

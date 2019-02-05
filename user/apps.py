from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"

    def ready(self):
        # pylint: disable=unused-import
        from user import signals

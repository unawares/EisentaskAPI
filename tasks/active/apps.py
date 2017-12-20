from django.apps import AppConfig


class ActiveConfig(AppConfig):
    name = 'tasks.active'

    def ready(self):
        import tasks.active.signals

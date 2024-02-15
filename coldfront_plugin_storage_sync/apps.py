from django.apps import AppConfig

class StorageSyncConfig(AppConfig):
    name = 'coldfront_plugin_storage_sync'

    def ready(self):
        from . import signals

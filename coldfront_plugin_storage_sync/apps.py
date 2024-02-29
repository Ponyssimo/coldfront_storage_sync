from django.apps import AppConfig

class StorageSyncConfig(AppConfig):
    name = 'coldfront_plugin_storage_sync'

    def ready(self):
        import coldfront_plugin_storage_sync.signals

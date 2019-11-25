from django.apps import AppConfig


class IsgmstoreConfig(AppConfig):
    name = 'ISGMStore'
    def ready(self):
        import ISGMStore.signals
        AppConfig.ready(self)
        print("Ready")
from django.apps import AppConfig


class hotelConfig(AppConfig):
    name = 'hotel'

    def ready(self):
        import hotel.signals

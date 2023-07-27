from django.conf import settings


class DBRouter:

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

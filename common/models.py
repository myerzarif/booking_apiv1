"""Models of Product App"""
import uuid
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    """
    Base Model
    """
    class Meta:
        ordering = ["-created_at"]
        abstract=True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def update(self, new_doc):
        for key, value in new_doc.items():
            setattr(self, key, value)
        self.save()
        return self
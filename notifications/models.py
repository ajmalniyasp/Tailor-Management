from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from foundations.models import BaseModel  # <-- your base model path adjust this


class Notification(BaseModel):  # <-- inherits auto_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor_ct = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    actor_id = models.PositiveIntegerField(null=True, blank=True)
    actor = GenericForeignKey("actor_ct", "actor_id")

    verb = models.CharField(max_length=120, null=True, blank=True)
    target_ct = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]


from django.db import models

# Create your models here.

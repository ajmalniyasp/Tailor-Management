from django.db import models
from django.conf import settings
from orders.models import Measurements
from foundations.models import BaseModel


class Feedback(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedback")
    order = models.ForeignKey(Measurements, on_delete=models.CASCADE, related_name="feedback")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comments = models.TextField(blank=True, null=True)

    def _str_(self):
        return f"{self.user.name} - {self.rating} Stars"
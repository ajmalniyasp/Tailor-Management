# notifications/utils.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_and_push_notification(
    *, user, verb: str, actor=None, target=None, url: str = "", payload: dict | None = None
):
    """
    Creates notification and pushes it to WS group:
    `user_{user.pk}`
    """

    actor_ct = ContentType.objects.get_for_model(actor) if actor else None
    target_ct = ContentType.objects.get_for_model(target) if target else None

    # ✅ auto_id is automatically created because Notification inherits BaseModel
    n = Notification.objects.create(
        user=user,
        verb=verb,
        url=url or "",
        payload=payload or {},
        actor_ct=actor_ct,
        actor_id=getattr(actor, "pk", None),
        target_ct=target_ct,
        target_id=getattr(target, "pk", None),
    )

    # ✅ Push via WebSocket using user group name
    channel_layer = get_channel_layer()
    group = f"user_{user.pk}"

    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": "notify",
            "data": {
                "id": n.auto_id,                         # ✅ ALWAYS SEND auto_id
                "verb": n.verb,
                "url": n.url,
                "created_at": n.created_at.isoformat(),
                "payload": n.payload,
            },
        },
    )

    return n
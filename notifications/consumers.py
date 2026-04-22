import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            self.group_name = f"user_{user.pk}"  # user.pk is correct here (user id)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close(code=4001)  # not authenticated

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        if user and getattr(self, "group_name", None):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        """
        Allow marking a notification as read through WS:
        {
            "action": "mark_read",
            "id": 12   <-- this will now be auto_id
        }
        """
        action = content.get("action")
        if action == "mark_read" and (nid := content.get("id")):
            await self.mark_read(nid)

    @database_sync_to_async
    def mark_read(self, notification_id: int):
        from .models import Notification
        try:
            # ✅ Replace pk with auto_id
            n = Notification.objects.get(auto_id=notification_id, user=self.scope["user"])
            if not n.is_read:
                n.is_read = True
                n.save(update_fields=["is_read"])
        except Notification.DoesNotExist:
            pass

    # Handler for group_send
    async def notify(self, event):
        """
        event = {
            "type": "notify",
            "data": {
                "id": <auto_id>,
                "verb": "New order assigned",
                ...
            }
        }
        """
        await self.send_json(event["data"])
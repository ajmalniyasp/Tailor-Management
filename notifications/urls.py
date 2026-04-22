# notifications/urls.py
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.list_notifications, name="list"),  # notifications/ page
    path("mark-read/<int:pk>/", views.mark_read, name="mark_read"),  # uses auto_id in view
    path("mark-all-read/", views.mark_all_read, name="mark_all_read"),
    path("unread-count/", views.unread_count, name="unread_count"),
]
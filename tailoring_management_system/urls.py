from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),

    path('auth/', include('allauth.urls')),

    path('', include('accounts.urls', namespace="accounts")),
    path('orders/', include('orders.urls', namespace="orders")),
    path('customer/', include('customers.urls')),
    path("notifications/", include("notifications.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

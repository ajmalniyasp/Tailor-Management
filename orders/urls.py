from django.urls import path
from .import views

app_name = "orders"

urlpatterns = [
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/add/', views.measurement_create, name='measurement_create'),
    path('measurements/<uuid:pk>/edit/', views.measurement_update, name='measurement_update'),
    path('measurements/<uuid:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    path('measurements/<uuid:pk>/', views.measurement_detail, name='measurement_detail'),

    path("dress-types/", views.dresstype_list, name="dresstype_list"),
    path("dress-types/add/", views.dresstype_create, name="dresstype_create"),
    path("dress-types/<uuid:pk>/edit/", views.dresstype_update, name="dresstype_update"),
    path("dress-types/<uuid:pk>/delete/", views.dresstype_delete, name="dresstype_delete"),

    path("get-fields/<uuid:dress_type_id>/", views.get_fields, name="get_fields"),

    path("orders/", views.order_list, name="order_list"),
    path("orders/new/", views.place_order, name="order_create"),

    path("add/<uuid:measurement_id>/", views.add_measurement_to_order, name="add_measurement_to_order"),
    path("view/<uuid:order_id>/", views.order_detail, name="order_detail"),
    path("update-quantity/<uuid:item_id>/", views.update_quantity, name="update_quantity"),
    path("item/<uuid:item_id>/cancel/", views.cancel_item, name="cancel_item"),
    path("confirm_order/<uuid:order_id>/", views.confirm_order, name="confirm_order"),





]

from django.urls import path
from . import views


app_name = "accounts"


urlpatterns = [
    path('redirect/', views.redirect_to_login, name='redirect_to_login'),
    path('', views.home_page, name='home_page'),
    path("tailor/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),

    path('staff/order/<uuid:order_id>/update/', views.staff_update_order, name='staff_update_order'),
    path("measurements/staff/view/<uuid:pk>/", views.measurement_detail_for_staff, name="staff_measurement_detail"),




    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('logout/', views.logout, name='logout'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    path('profile/', views.customer_profile, name='customer_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]

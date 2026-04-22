from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('submit/', views.submit_feedback, name='submit'),
    path('view/', views.feedback_list, name='view'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
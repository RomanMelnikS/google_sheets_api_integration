from django.urls import path

from google_sheets_service import views

urlpatterns = [
    path('', views.index, name='index')
]
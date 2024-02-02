from django.urls import path
from agrotourism import views

urlpatterns = [
    path('generate/', views.generate_agrotourism_content, name='generate_agrotourism_content'),
]

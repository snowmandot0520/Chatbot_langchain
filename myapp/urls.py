from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),      # Root URL (index page)
    path('chat/', views.chat, name='chat'),   # Chat URL
]

from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('chat/', views.chat_view, name='chat'),
    re_path(r'^.*/$', TemplateView.as_view(template_name='index.html')),

]

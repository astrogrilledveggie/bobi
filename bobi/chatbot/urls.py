from django.urls import path
from . import views
from .views import ChatterBotAppView, ChatterBotApiView

app_name = 'chatbot/'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', ChatterBotAppView.as_view(), name='chatbot-app'),
    path('api/', ChatterBotApiView.as_view(), name='chatbot-api'),
]
"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from .views import ChatterBotAppView, ChatterBotApiView, send

app_name = 'chatbot/' # route namespacing i.e. setting /chatbot as home directory

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', ChatterBotAppView.as_view(), name='chatbot-app'),
    path('app/send', send, name='send'),
    path('api/', ChatterBotApiView.as_view(), name='chatbot-api'),
]
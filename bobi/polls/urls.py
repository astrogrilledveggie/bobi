from django.urls import path

from . import views

app_name = 'polls' # route namespacing i.e. setting /polls as home directory

urlpatterns = [
    path('', views.index, name='index'),
    path('questions', views.list_questions, name='list_questions'),
    path('<int:question_id>', views.detail, name='detail'),
    path('<int:question_id>/vote', views.vote, name='vote'),
]

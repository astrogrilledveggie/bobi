from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as core_views

app_name = 'accounts/'

urlpatterns = [
    path('', core_views.index, name="index"),
    path('login/', core_views.acctlogin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('signup/', core_views.signup, name='signup'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(), name='passwordchange'),
]
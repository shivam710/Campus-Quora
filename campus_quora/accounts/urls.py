from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [

    path(r'signup/', views.signup, name='signup'),
    path(r'', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'/(?P<username>[\w.@+-]+)/choose/', views.choose, name='choose'),
]

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [

    # admin-page
    path('admin/', admin.site.urls),

    # for sign-up
    path(r'', include('accounts.urls', namespace = 'accounts')),

    # for blogs
    path(r'blogs/', include('blog.urls', namespace = 'blog')),
    # home-page
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),

    #path('(?P<user_id>[0-9]+)/', TemplateView.as_view(template_name='myques.html',{}), name='myques'),
]

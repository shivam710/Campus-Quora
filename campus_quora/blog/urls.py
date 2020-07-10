from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "blog"

urlpatterns = [
    path(r'(?P<username>[\w.@+-]+)/', views.homepage, name='home'),
    path(r'(?P<username>[\w.@+-]+)/search/', views.search, name='search'),
    path(r'(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/ssearch/', views.ssearch, name='ssearch'),
    path(r'(?P<username>[\w.@+-]+)/mysearch/', views.mysearch, name='mysearch'),
    path(r'(?P<username>[\w.@+-]+)/settings/', views.settings, name='settings'),
    path(r'(?P<username>[\w.@+-]+)/preferences/', views.preferences, name='preferences'),
    path(r'(?P<username>[\w.@+-]+)/updatepreferences/', views.updatepreferences, name='updatepreferences'),
    path(r'(?P<username>[\w.@+-]+)/bookmarksearch/', views.bookmarksearch, name='bookmarksearch'),
    path(r'(?P<username>[\w.@+-]+)/(?P<username2>[\w.@+-]+)/userinfo/', views.userinfo, name='userinfo'),
    path(r'(?P<username>[\w.@+-]+)/myques/', views.myques, name='myques'),
    path(r'(?P<username>[\w.@+-]+)/myans/', views.myans, name='myans'),
    path(r'(?P<username>[\w.@+-]+)/question/add/', views.QuestionCreate, name='ques_add'),
    path(r'(?P<username>[\w.@+-]+)/(?P<pk>[0-9]+)/(?P<pk2>[0-9]+)/answer/add/', views.AnswerCreate, name='ans_add'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/question/vote/', views.vote, name='vote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/question/ans/', views.ans, name='ans'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/question/sortans/', views.sortans, name='sortans'),
    path(r'(?P<username>[\w.@+-]+)/sortques/', views.sortques, name='sortques'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/deleteques/(?P<pk2>[0-9]+)/', views.deleteques, name='deleteques'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/deleteques/(?P<search>[\w.@+-]+)/search', views.sdeleteques, name='sdeleteques'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/qs_deleteques/', views.qs_deleteques, name='qs_deleteques'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/ansdelete/(?P<pk2>[0-9]+)/(?P<pk3>[0-9]+)', views.ansdelete, name='ansdelete'),
    path(r'(?P<username>[\w.@+-]+)/notification/', views.notification, name='notification'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<pk2>[0-9]+)/bookmark/', views.bookmark, name='bookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/sbookmark/', views.sbookmark, name='sbookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/qs_bookmark/', views.qs_bookmark, name='qs_bookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nbookmark/', views.nbookmark, name='nbookmark'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<pk2>[0-9]+)/removebookmark/', views.removebookmark, name='removebookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/sremovebookmark/', views.sremovebookmark,name='sremovebookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/qs_removebookmark/', views.qs_removebookmark,name='qs_removebookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/(?P<search>[\w.@+-]+)/bs_removebookmark/', views.bs_removebookmark,name='bs_removebookmark'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nremovebookmark/', views.nremovebookmark, name='nremovebookmark'),

    path(r'(?P<username>[\w.@+-]+)/mybookmark/', views.mybookmark, name='mybookmark'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/quesvote/(?P<pk2>[0-9]+)/', views.quesvote, name='quesvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/squesvote/(?P<search>[\w.@+-]+)/', views.squesvote, name='squesvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/bs_quesvote/(?P<search>[\w.@+-]+)/', views.bs_quesvote, name='bs_quesvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/qs_quesvote/(?P<search>[\w.@+-]+)/', views.qs_quesvote, name='qs_quesvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nquesvote/', views.nquesvote, name='nquesvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nansvote/', views.nansvote, name='nansvote'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/quesdownvote/(?P<pk2>[0-9]+)/', views.quesdownvote, name='quesdownvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/squesdownvote/(?P<search>[\w.@+-]+)/', views.squesdownvote,name='squesdownvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/bs_quesdownvote/(?P<search>[\w.@+-]+)/', views.bs_quesdownvote,name='bs_quesdownvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/qs_quesdownvote/(?P<search>[\w.@+-]+)/', views.qs_quesdownvote,name='qs_quesdownvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/quesdownvote/', views.nquesdownvote,name='nquesdownvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nansdownvote/', views.nansdownvote, name='nansdownvote'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/ansvote/(?P<pk2>[0-9]+)/', views.ansvote, name='ansvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/ansdownvote/(?P<pk2>[0-9]+)/', views.ansdownvote, name='ansdownvote'),

    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/allvote/', views.allvote, name='allvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/allansvote/', views.allansvote, name='allansvote'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/nques/', views.nques, name='nques'),
    path(r'(?P<pk>[0-9]+)/(?P<username>[\w.@+-]+)/ndelete/', views.ndelete, name='ndelete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
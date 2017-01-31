from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^get_new_articles/$', views.get_new_articles, name="get_new_articles"),
    url(r'^newsreel/$', views.newsreel, name="newsreel"),
    url(r'^share/(?P<id>\d+)$', views.share, name="share"),
    url(r'^like_article/(?P<id>\d+)$', views.like_article, name="like_article"),
    url(r'^unlike/(?P<id>\d+)$', views.unlike, name="unlike"),
]

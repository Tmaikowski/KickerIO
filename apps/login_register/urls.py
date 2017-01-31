from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register/$', views.register, name="register"),
    url(r'^process_login/$', views.process_login, name="process_login"),
    url(r'^process_registration/$', views.process_registration, name="process_registration"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^account/(?P<id>\d+)$', views.account, name="account_settings"),
    url(r'^account/edit/(?P<id>\d+)$', views.edit, name="edit"),
    url(r'^account/update/(?P<id>\d+)$', views.update_account, name="update_account"),
    url(r'^follow/(?P<id>\d+)$', views.follow, name="follow"),
    url(r'^profile/(?P<id>\d+)$', views.profile, name="profile"),
]

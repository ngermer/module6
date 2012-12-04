from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
    url(r'^$', 'phototagz.views.index'),
    url(r'^tag/(?P<tag_id>\d+)/(?P<image_id>\d+)/$', 'phototagz.views.tagview'),
    url(r'^addimg/$', 'phototagz.views.imageaddformview'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/register/$', 'phototagz.views.register_user_form'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/photo/accounts/login/'}),
    url(r'^accounts/change_password/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/photo/'}),
    url(r'^accounts/reset_password/$', 'django.contrib.auth.views.password_reset'),
    url(r'^accounts/reset_password_done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^accounts/change_password/done/$', 'django.contrib.auth.views.password_change_done'),
)


"""thiamsu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^song/(?P<id>[0-9]*)/$', views.song_detail, name='song_detail'),
    url(r'^song/(?P<id>[0-9]*)/edit/$', views.song_edit, name='song_edit'),
    url(r'^song/(?P<id>[0-9]*)/translation/$', views.song_translation_post, name='song_translation_post'),
    url(r'^user/(?P<id>[0-9]+)/$', views.user_profile, name='user_profile'),
    url(r'^chart/$', views.chart, name='chart'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^api/user/favorite_song/$', views.api_user_favorite_song, name='api_user_favorite_song'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

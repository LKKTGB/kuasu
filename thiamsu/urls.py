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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.home, name="home"),
    re_path(r"^form/account_deletion", views.account_deletion, name="account_deletion"),
    re_path(r"^policies/privacy", views.privacy_policy, name="policy_privacy"),
    re_path(r"^search/$", views.search, name="search"),
    re_path(r"^song/(?P<id>[0-9]*)/$", views.song_detail, name="song_detail"),
    re_path(r"^song/(?P<id>[0-9]*)/edit/$", views.song_edit, name="song_edit"),
    re_path(
        r"^song/(?P<id>[0-9]*)/translation/$",
        views.song_translation_post,
        name="song_translation_post",
    ),
    re_path(r"^user/(?P<id>[0-9]+)/$", views.user_profile, name="user_profile"),
    re_path(r"^chart/$", views.chart, name="chart"),
    re_path(r"^grappelli/", include("grappelli.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),
    re_path(
        r"^api/user/favorite_song/$",
        views.api_user_favorite_song,
        name="api_user_favorite_song",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [re_path(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

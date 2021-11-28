
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("make_posting", views.make_posting, name="make_posting"),
    path("view_all_post", views.view_all_post, name="view_all_post"),
    path("view_profile", views.view_profile, name="view_profile"),
    path("thumbs_click", views.thumbs_click, name="thumbs_click"),
    path("follows", views.follows, name="follows"),
    path("followings", views.followings, name="followings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

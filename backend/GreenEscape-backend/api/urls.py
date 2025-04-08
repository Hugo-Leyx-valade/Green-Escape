from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin




urlpatterns = [
    path('', views.play_screen),
    path('generate_maze', views.generate_maze_view),
    path('admin/', admin.site.urls),
    path("register/", views.register, name="register"),  # API (POST)
    path("register-page/", views.register_page, name="register_page"),
    path("login-page/", views.login_page, name="login"),
    path("login/", views.login_view, name="login"),
    path("check-login/", views.check_session, name="check_login"),
    path("logout/", views.logout_view, name="logout"),
    path("auth-page/", views.auth_page),
    path("profile/", views.profile),
    path("data-profile/", views.retieveUserData),
    path("scoreboard/", views.showScoreboard),
    path("saveTime/", views.saveBestTime)
]

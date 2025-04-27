from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import edit_profile




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
    path("edit-profile/", edit_profile, name="edit-profile"),
    path("scoreboard/", views.scoreboard, name="scoreboard"),
    path("hub/", views.hub, name="hub"),
    path("update-stats/", views.update_player_stats, name="update_player_stats"),
    path('scoreboard-by-seed/', views.scoreboard_by_seed, name='scoreboard_by_seed'),
    path('save-best-time/', views.saveBestTime, name='saveBestTime'),
    path('save-best-time/<int:seed>/', views.saveBestTime, name='saveBestTime'),
]

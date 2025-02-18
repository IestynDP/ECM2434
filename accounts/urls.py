from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name="home"),
    path("points/", views.points_view, name="points"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("search/", views.search_users, name="search_users"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
]


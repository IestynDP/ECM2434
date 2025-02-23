from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name="home"),
    path("points/", views.points_view, name="points"),
    path("edit-profile/<str:username>/", views.edit_profile, name="edit_profile_with_username"),
    path("search/", views.search_users, name="search_users"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.profile_view, name="profile_with_username"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("download-data/", views.download_data, name="download_data"),
]


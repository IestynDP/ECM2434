from django.urls import path
from apps.accounts import views  # Updated path
from . import views
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name="home"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("edit-profile/<str:username>/", views.edit_profile, name="edit_profile_with_username"),
    path("search/", views.search_users, name="search_users"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.profile_view, name="profile_with_username"),
    path("add-restaurant/", views.add_restaurant, name="add_restaurant"),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path("items-management/", views.manage_items, name="manage-items"),
    path("restaurants/", views.restaurant_list, name="restaurant_list"),
    path("check-in/<int:restaurant_id>/", views.check_in, name="check_in"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("download-data/", views.download_data, name="download_data"),
    path("info/", views.info, name="info"),
    path('restaurants/<int:restaurant_id>/', views.restaurant_details, name='restaurant_details'),
    path('qr_scanner/', include('apps.qr_scanner.urls')),
    path("profile-redirect/", views.profile_redirect, name="profile_redirect")

    path("check-in/<int:restaurant_id>/", views.check_in, name="check_in"),
]


from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.people, name='people'),
    path('search-users/', views.search_users, name='search_users'),
    path('<str:username>/follow/', views.follow_user, name='follow_user'),
    path('<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]
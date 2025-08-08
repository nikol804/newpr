from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('user/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    
    # AJAX endpoints
    path('api/find-match/', views.find_match, name='find_match'),
    path('api/update-test-scores/', views.update_test_scores, name='update_test_scores'),
]

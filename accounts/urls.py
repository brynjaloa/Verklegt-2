# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('check-username/', views.check_username_view, name='check_username'),
    path('check-email/', views.check_email_view, name='check_email'),
    path(
        'login/',
        LoginView.as_view(
            template_name='accounts/login.html',
            next_page='profile',
            redirect_authenticated_user=True,
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('sellers/<int:seller_id>/', views.seller_profile_view, name='seller_profile'),
    path('become-seller/', views.become_seller_view, name='become_seller'),
]

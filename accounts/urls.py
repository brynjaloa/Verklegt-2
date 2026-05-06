from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
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
    path('become-seller/', views.become_seller_view, name='become_seller'),
]

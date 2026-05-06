from django.urls import path, include
from . import views

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
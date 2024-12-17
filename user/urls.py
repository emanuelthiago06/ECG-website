from django.urls import path
from . import views

urlpatterns=[
    path('login', views.login_page, name= "login"),
    path('logout', views.logout_user, name= "logout"),
    path('handle_login', views.handle_login, name='handle_login'),
    path('sign_in', views.sign_in, name="sign_in"),
    path('handle_sign_in', views.handle_sign_in, name="handle_sign_in")
]
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('logout/', views.signoff, name="logout"),
    path('menu/', views.search_food, name="menu"),
    path('order/', views.order, name="order"),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/confirmation/', views.password_reset_confirmation, name='password_reset_confirmation'),

    path('payment/', views.payment, name="payment"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),


]

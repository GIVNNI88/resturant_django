from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('myinfo/', views.user_info, name="myinfo"),
    path('categories/', views.categories, name="categories"),
    path('category/<int:id>', views.show_by_category, name="category"),
    path('add_to_cart/', views.add_to_cart, name="add"),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name="remove"),
    path('edit_my_info/', views.edit_my_info, name="edit"),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('my_deliveries/', views.my_deliveries, name="mydeliveries"),

]

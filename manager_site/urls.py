from django.urls import path
from . import views

urlpatterns = [
    path('login_manager/', views.login_manager, name="login_manager"),
    path('add_category/',views.add_category,name="add_category"),
    path('add_dish/',views.add_dish,name="add_dish"),
    path('edit_category/<int:id>', views.edit_category, name="edit_cat"),
    path('delete_category/<int:id>', views.delete_category, name="del_cat"),
    path('edit_dish/<int:id>', views.edit_dish, name="edit_dish"),
    path('delete_dish/<int:id>', views.delete_dish, name="del_dish"),
    path('confirm_delivery/<int:id>', views.confirm_delivery, name="confirm_del"),
    path('manage_delivery/', views.manage_delivery, name="manage_del"),
    path('confirm_manager/<int:id>', views.confirm_manager, name="confirm_manager"),
    path('manage_user/', views.manage_user, name="manage_user")
]
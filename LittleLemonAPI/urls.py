from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #User sección
    path('users/', views.UsersView, name='users'),
    path('users/users/me/', views.UserView, name='user'),
    path('token/login/', obtain_auth_token, name='login'),
    
    #Menu sección
    path('menu-items/', views.MenuItemsView, name='menu-items'),
    path('menu-items/<int:pk>/', views.MenuItemView, name='menu-item'),
    path('category/', views.categoriesView, name='category'),
    path('category/<int:pk>/', views.categoryView, name='category-detail'),
    
    #path('categories/', views.CategoriesView.as_view(), name='categories'),
    #path('carts/', views.CartsView.as_view(), name='carts'),
    #path('orders/', views.OrdersView.as_view(), name='orders'),
    #path('order_items/', views.OrderItemsView.as_view(), name='order_items'),
    
    
    path('newmanager/', views.newManager, name='newManager'),
    path('managerlist/', views.managerList, name='managerList'),
    path('newdeliverymember/', views.newDeliveryMember, name='newDeliveryMember'),
    path('assignDeliveryMember/<int:pk>/', views.assignDeliveryMember, name='assignDeliveryMember'),
]
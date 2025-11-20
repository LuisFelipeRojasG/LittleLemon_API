from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #User sección
    path('users/', views.UsersView, name='users'),
    path('users/users/me/', views.UserView, name='user'),
    path('token/login/', obtain_auth_token, name='login'),
    
    path('groups/manager/users/', views.managerListView, name='manager'),
    path('groups/manager/users/<int:pk>/', views.managerView, name='manager'),
    
    path('groups/delivery-crew/users/', views.deliveryCrewListView, name='delivery-crew'),
    path('groups/delivery-crew/users/<int:pk>/', views.deliveryCrewView, name='delivery-crew'),
    
    #Menu sección
    path('menu-items/', views.MenuItemsView, name='menu-items'),
    path('menu-items/<int:pk>/', views.MenuItemView, name='menu-item'),
    path('category/', views.categoriesView, name='category'),
    path('category/<int:pk>/', views.categoryView, name='category-detail'),
    
    #Cart sección
    path('cart/menu-items', views.CartView, name='cart'),
    
    #Order sección
    path('orders/', views.OrderView, name='orders'),
    path('orders/<int:pk>/', views.OrderView, name='order'),
    
]
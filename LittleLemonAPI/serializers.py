from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem, User

#User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'description', 'featured', 'day_choice', 'category']


class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()
    )
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        allow_null=True,
        required=False
    )
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        
        
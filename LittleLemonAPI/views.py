from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User

# User Views
@api_view(['POST'])
def UsersView(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response({"message": "Username, email, and password are required."}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists."}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": f"User {user.username} created successfully."}, status=201)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserView(request):
    if (request.user.is_authenticated):
        user = request.user
        return Response({"username": user.username, "email": user.email}, status=200)
    else:
        return Response({"message": "You are not authenticated!"}, status=403)
    
    
# Menu sección
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def MenuItemsView(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=200)
    if request.user.groups.filter(name='Manager').exists():
        #Se obtiene el nombre del producto del cuerpo de la solicitud
        item_name = request.data.get('title')
        #Se crea un nuevo elemento del menú
        menuItem = MenuItem.objects.create(title=item_name, price=request.data.get('price'), featured=request.data.get('featured', False),
                                           day_choice=request.data.get('day_choice', False),
                                           category=Category.objects.get(slug=request.data.get('category_slug')))
        return Response({"message": f"Menu Item {menuItem.title} created successfully."}, status=201)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
    
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def MenuItemView(request, pk):
    if request.method == 'GET':
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=200)
    elif request.user.groups.filter(name='Manager').exists():
        if request.method == 'PUT' or request.method == 'PATCH':
            menu_item = get_object_or_404(MenuItem, pk=pk)
            menu_item.title = request.data.get('title', menu_item.title)
            menu_item.price = request.data.get('price', menu_item.price)
            menu_item.featured = request.data.get('featured', menu_item.featured)
            menu_item.day_choice = request.data.get('day_choice', menu_item.day_choice)
            if 'category_slug' in request.data:
                menu_item.category = Category.objects.get(slug=request.data.get('category_slug'))
            menu_item.save()
            return Response({"message": f"Menu Item {menu_item.title} updated successfully."}, status=200)
        elif request.method == 'DELETE':
            menu_item = get_object_or_404(MenuItem, pk=pk)
            menu_item.delete()
            return Response({"message": f"Menu Item {menu_item.title} deleted successfully."}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
        

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categoriesView(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=200)
        elif request.method == 'POST':
            #Se obtiene el nombre de la categoría del cuerpo de la solicitud
            category_title = request.data.get('title')
            #Se crea una nueva categoría
            category = Category.objects.create(title=category_title, slug=category_title.lower().replace(" ", "-"))
            return Response({"message": f"Category {category.title} created successfully."}, status=201)
    else:
        return Response({"message": "You are not authorized!"}, status=403)

@api_view(['PATCH', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def categoryView(request, pk):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'PATCH':
            category = get_object_or_404(Category, pk=pk)
            category.title = request.data.get('title', category.title)
            category.slug = request.data.get('slug', category.slug)
            category.save()
            return Response({"message": f"Category {category.title} updated successfully."}, status=200)
        elif request.method == 'DELETE':
            category = get_object_or_404(Category, pk=pk)
            category.delete()
            return Response({"message": f"Category {category.title} deleted successfully."}, status=200)
        elif request.method == 'GET':
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)









@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newManager(request):
    if request.user.groups.filter(name='Administrator').exists():
        #Se obtiene el nombre de usuario y se verifica si el usuario existe
        user = get_object_or_404(User, username=request.data.get('username'))
        #Se verifica si el grupo Manager existe
        group_name = get_object_or_404(Group, name="Manager")
        
        user.groups.add(group_name)
        user.save()
        return Response({"message": f"User {user.username} added to group {group_name}."}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def managerList(request):
    if request.user.groups.filter(name='Administrator').exists():
        #Se obtiene el grupo de gerentes
        manager_group = Group.objects.get(name='Manager')
        #Se filtran los usuarios que pertenecen al grupo de gerentes
        managers = User.objects.filter(groups=manager_group)
        manager_usernames = [manager.username for manager in managers]
        return Response({"managers": manager_usernames}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
    

    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newDeliveryMember(request):
    if request.user.groups.filter(name='Manager').exists():
        #Se obtiene el nombre de usuario y se verifica si el usuario existe
        user = get_object_or_404(User, username=request.data.get('username'))
        #Se verifica si el grupo Manager existe
        group_name = get_object_or_404(Group, name="Delivery_crew")
        
        user.groups.add(group_name)
        user.save()
        return Response({"message": f"User {user.username} added to group {group_name}."}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def assignDeliveryMember(request, pk):
    if request.user.groups.filter(name='Manager').exists():
        order = get_object_or_404(Order, pk=pk)
        delivery_member = get_object_or_404(User, username=request.data.get('username'))
        if delivery_member.groups.filter(name='Delivery_crew').exists():
            order.delivery_crew = delivery_member
            order.save()
            return Response({"message": f"Delivery member {delivery_member.username} assigned to order {order.id}."}, status=200)
        else:
            return Response({"message": "The specified user is not a delivery crew member!"}, status=400)
    else:
        return Response({"message": "You are not authorized!"}, status=403)

    
    

    
"""

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#Para listar y crear elementos del menú
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    

class CartsView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    
class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
class OrderItemsView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer"""
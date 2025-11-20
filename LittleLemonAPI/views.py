from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage

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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def managerListView(request):
    if request.user.groups.filter(name='Administrator').exists() or request.user.groups.filter(name='Manager').exists():
        #Se obtiene el grupo de gerentes
        manager_group = Group.objects.get(name='Manager')
        #Se filtran los usuarios que pertenecen al grupo de gerentes
        managers = User.objects.filter(groups=manager_group)
        manager_usernames = [manager.username for manager in managers]
        return Response({"managers": manager_usernames}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
        
    
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def managerView(request, pk):
    if request.user.groups.filter(name='Administrator').exists() or request.user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            #Se verifica si el grupo Manager existe
            group_name = get_object_or_404(Group, name="Manager")
            user.groups.add(group_name)
            user.save()
            return Response({"message": f"User {user.username} created {group_name}."}, status=201)
        elif request.method == 'DELETE':
            user.groups.clear()
            user.save()
            return Response({"message": f"User {user.username} removed from all groups."}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deliveryCrewListView(request):
    if request.user.groups.filter(name='Administrator').exists() or request.user.groups.filter(name='Manager').exists():
        #Se obtiene el grupo de delivery crew
        delivery_crew_group = Group.objects.get(name='Delivery_crew')
        #Se filtran los usuarios que pertenecen al grupo de delivery crew
        delivery_crews = User.objects.filter(groups=delivery_crew_group)
        delivery_crew_usernames = [delivery_crew.username for delivery_crew in delivery_crews]
        return Response({"delivery_crews": delivery_crew_usernames}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)
    
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def deliveryCrewView(request, pk):
    if request.user.groups.filter(name='Administrator').exists() or request.user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            #Se verifica si el grupo Delivery_crew existe
            group_name = get_object_or_404(Group, name="Delivery_crew")
            user.groups.add(group_name)
            user.save()
            return Response({"message": f"User {user.username} added to group {group_name}."}, status=201)
        elif request.method == 'DELETE':
            user.groups.clear()
            user.save()
            return Response({"message": f"User {user.username} removed from all groups."}, status=200)
    else:
        return Response({"message": "You are not authorized!"}, status=403)

    
# Menu sección
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def MenuItemsView(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        search = request.query_params.get('search')
        perpage = request.query_params.get('perpage', default=3)
        page = request.query_params.get('page', default=1)
        if category_name:
            menu_items = menu_items.filter(category__title__iexact=category_name)
        if price:
            menu_items = menu_items.filter(price__lte=price)
        if search:
            menu_items = menu_items.filter(title__icontains=search)
        paginator = Paginator(menu_items, perpage)
        try:
            menu_items = paginator.page(page)
        except EmptyPage:
            menu_items = []
            
        
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=200)
    if request.user.groups.filter(name='Manager').exists():
        #Se obtiene el nombre del producto del cuerpo de la solicitud
        item_name = request.data.get('title')
        #Se crea un nuevo elemento del menú
        menuItem = MenuItem.objects.create(title=item_name, price=request.data.get('price'), 
                                           description=request.data.get('description'), 
                                           featured=request.data.get('featured', False),
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


#Cart sección
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def CartView(request):
    user = request.user
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=200)
    
    elif request.method == 'POST':
        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity', 1)
        
        if not menuitem_id or not quantity:
            return Response({"message": "menuitem and quantity are required."}, status=400)
        
        menuitem = get_object_or_404(MenuItem, id=menuitem_id)
        
        # Verificar si el item ya existe en el carrito
        cart_item = Cart.objects.filter(user=user, menuitem=menuitem).first()
        
        if cart_item:
            # Si existe, incrementar cantidad
            cart_item.quantity += int(quantity)
            cart_item.save()
            return Response({"message": f"Item {menuitem.title} quantity updated."}, status=200)
        else:
            # Si no existe, crear nuevo item en carrito
            cart_item = Cart.objects.create(
                user=user,
                menuitem=menuitem,
                quantity=int(quantity),
                unit_price=menuitem.price,
                price=menuitem.price * int(quantity)
            )
            return Response({"message": f"Item {menuitem.title} added to cart."}, status=201)
    elif request.method == 'DELETE':
        # Eliminar todos los items del carrito del usuario
        Cart.objects.filter(user=user).delete()
        return Response({"message": "All items removed from cart."}, status=200)


#Order sección
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def OrderView(request, pk=None):
    user = request.user
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            if pk:
                # Obtener una orden específica
                order = get_object_or_404(Order, pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=200)
            else:
                # Obtener todas las órdenes
                orders = Order.objects.all()
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=200)
        elif request.method == 'PATCH':
            # Actualizar una orden existente
            order = get_object_or_404(Order, pk=pk)
            order.status = request.data.get('status', order.status)
            order.total = request.data.get('total', order.total)
            order.date = request.data.get('date', order.date)
            order.save()
            return Response({"message": f"Order {order.id} updated successfully."}, status=200)

        elif request.method == 'DELETE':
            # Eliminar una orden existente
            order = get_object_or_404(Order, pk=pk)
            order.delete()
            return Response({"message": f"Order {order.id} deleted successfully."}, status=200)
    elif request.user.groups.filter(name='Delivery_crew').exists():
        if request.method == 'GET':
            if pk:
                # Obtener una orden específica
                order = get_object_or_404(Order, pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=200)
            else:
                # Obtener todas las órdenes
                orders = Order.objects.all()
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=200)
        elif request.method == 'PATCH':
            # Actualizar el estado de una orden existente
            order = get_object_or_404(Order, pk=pk)
            order.status = request.data.get('status', order.status)
            order.save()
            return Response({"message": f"Order {order.id} status updated successfully."}, status=200)
    elif not request.user.groups.filter(name='Maneger').exists() or not request.user.groups.filter(name='Delivery_crew').exists():
        if request.method == 'GET':
            if pk:
                # Obtener una orden específica
                order = get_object_or_404(Order, pk=pk, user=user)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=200)
            else:
                # Obtener todas las órdenes del usuario
                orders = Order.objects.filter(user=user)
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=200)

        elif request.method == 'POST':
            # Crear una nueva orden
            total = request.data.get('total')
            date = request.data.get('date')
            
            if not total or not date:
                return Response({"message": "Total and date are required."}, status=400)
            
            order = Order.objects.create(user=user, total=total, date=date)
            return Response({"message": f"Order created successfully with ID {order.id}."}, status=201)
        
        return Response({"message": "You are not authorized!"}, status=403)








    

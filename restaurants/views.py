from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Restaurant, Dish, CustomUser
from .serializers import RestaurantSerializer, DishSerializer, CustomUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, password=password, email=email, phone_number=phone_number, address=address)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

class DishList(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Verifica si se proporciona un restaurantId en la URL
        restaurant_id = self.kwargs.get('restaurantId')
        if restaurant_id:
            # Filtra los platos por el restaurante especificado
            return Dish.objects.filter(restaurant_id=restaurant_id)
        # Si no se proporciona un restaurantId, devuelve todos los platos
        return Dish.objects.all()

    def perform_create(self, serializer):
        # Obtén el ID del restaurante desde los datos de la solicitud
        restaurant_id = self.request.data.get('restaurant')
        try:
            # Busca el restaurante correspondiente
            restaurant = Restaurant.objects.get(id=restaurant_id)
            # Guarda el plato asociado al restaurante
            serializer.save(restaurant=restaurant)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_400_BAD_REQUEST)

class DishDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Obtén el ID del restaurante desde los datos de la solicitud
        restaurant_id = self.request.data.get('restaurant')
        try:
            # Busca el restaurante correspondiente
            restaurant = Restaurant.objects.get(id=restaurant_id)
            # Actualiza el plato asociado al restaurante
            serializer.save(restaurant=restaurant)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_400_BAD_REQUEST)
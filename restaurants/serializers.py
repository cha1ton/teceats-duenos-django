from rest_framework import serializers
from .models import Restaurant, Dish, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'address')

class DishSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)  # Campo opcional para la URL de la imagen

    class Meta:
        model = Dish
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)  # Campo opcional para la URL de la imagen

    class Meta:
        model = Restaurant
        fields = '__all__'
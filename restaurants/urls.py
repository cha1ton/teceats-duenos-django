from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('', views.RestaurantList.as_view(), name='restaurant_list'),
    path('<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('dishes/', views.DishList.as_view(), name='dish_list'),
    path('dishes/<int:pk>/', views.DishDetail.as_view(), name='dish_detail'),
    path('<int:restaurantId>/dishes/', views.DishList.as_view(), name='restaurant_dish_list')

]
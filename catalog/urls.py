from django.urls import path, re_path
from .views import category_list, product_list, product_detail, order_success, order_list_of_all_users, order_create, wish_list, wish_like, wish_dislike, order_list_user_self, user_reviews, calculate_order_cost

urlpatterns = [
    path('categories', category_list, name='category_list'),
    path('category/<slug:category_slug>/', product_list, name='product_list'),  
    path('product/<slug:product_slug>/', product_detail, name='product_detail'),
    path('order/create/', order_create, name='order_create'),
    path('order/success/', order_success, name='order_success'),
    path('order/calculate_cost/', calculate_order_cost, name='calculate_order_cost'),
    path('orders_of_users/', order_list_of_all_users, name='order_list_of_all_users'),
    path('my_orders/', order_list_user_self, name='order_list_user_self'),
    path('my-reviews/', user_reviews, name='user_reviews'),
    path('wishes/', wish_list, name='wish_list'),
    path('wishes/like/', wish_like, name='wish_like'),
    path('wishes/dislike/', wish_dislike, name='wish_dislike'),  
]

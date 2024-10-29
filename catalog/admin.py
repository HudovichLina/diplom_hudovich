from django.contrib import admin
from .models import Category, Product, Decoration, Order, OrderItem, Review, Wish
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'price')  
    list_filter = ('category', 'price' )
    list_editable = ['price']  
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description','slug', 'price') 

@admin.register(Decoration)
class DecorationAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_method', 'created_at')
    list_filter = ('delivery_method',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price') 
    search_fields = ('order__id', 'product__name') 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at') 
    search_fields = ('product__name',)  

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'likes', 'dislikes') 
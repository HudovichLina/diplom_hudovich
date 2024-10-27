from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, default="default-slug") 

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, default="slug") 
    ingredients = models.TextField(default="default")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail',
                        args=[self.slug])

class Decoration(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декоры'

    def __str__(self):
        return f"{self.name} ({self.description}) - {self.price} бел.руб."
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=50, choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')])
    delivery_address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username} - {self.delivery_method} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="1")
    weight = models.FloatField(null=True, blank=True) 
    quantity = models.PositiveIntegerField(null=True, blank=True) 
    decoration = models.ForeignKey(Decoration, null=True, blank=True, on_delete=models.SET_NULL)
    wishes = models.TextField(blank=True)  
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    decoration_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f"{self.product.name} in {self.order}"
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', default="2")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="null")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} о {self.product.name}"


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishes")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.description[:20]}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10)  # 'like' или 'dislike'
    
    class Meta:
        unique_together = (('user', 'wish'),)  # Уникальное сочетание пользователь-пожелание
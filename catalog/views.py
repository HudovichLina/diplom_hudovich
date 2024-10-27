from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import re

from .models import Category, Product, Order, OrderItem, Wish, Review, Vote, Decoration
from .forms import OrderForm, WishForm, ReviewForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    products = category.products.all()
    return render(request, 
                  'product_list.html', 
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_slug=product.slug)
    else:
        form = ReviewForm()

    return render(request, 
                  'product_detail.html', 
                  {'product': product, 
                   'reviews': reviews,
                   'form': form})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            product = form.cleaned_data['product']
            weight = form.cleaned_data['weight']
            quantity = form.cleaned_data['quantity']
            decoration = form.cleaned_data['decoration']
            product_price = product.price
            decoration_price = decoration.price if decoration else 0

            order_item = OrderItem(
                order=order,
                product=product,
                weight=weight,
                quantity=quantity,
                decoration=decoration,
                wishes=form.cleaned_data['wishes'],
                product_price=product_price,
                decoration_price=decoration_price,
                total_price = (product_price * (Decimal(weight) if weight else Decimal(quantity)) + decoration_price)
            )
            order_item.save()

            return redirect('order_success') 
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})


def order_success(request):
    return render(request, 'order_success.html')

@login_required
def calculate_order_cost(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        weight = request.POST.get('weight')
        if not weight or Decimal(weight) <= 0:
            return JsonResponse({'error': 'Invalid weight'}, status=400)
        quantity = request.POST.get('quantity')
        decoration_id = request.POST.get('decoration_id')
        
        product = Product.objects.get(id=product_id)
        decoration = Decoration.objects.get(id=decoration_id) if decoration_id else None

        product_price = product.price
        decoration_price = decoration.price if decoration else 0

        print(f"Product ID: {product_id}, Category: {product.category.id}, Weight: {weight}, Quantity: {quantity}, Decoration ID: {decoration_id}")  # Отладка

        # Логика расчета стоимости
        if product.category.name == 'Торты':
            try:
                total_price = decoration_price + (product_price * Decimal(weight) * Decimal(quantity))
            except InvalidOperation:
                return JsonResponse({'error': 'Invalid weight or quantity'}, status=400)
        else:
            total_price = decoration_price + (product_price * int(quantity))

        return JsonResponse({'total_price': total_price.quantize(Decimal('0.01'))})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@staff_member_required
def order_list_of_all_users(request):
    orders = Order.objects.all()
    return render(request, 'order_list_of_all_users.html', {'orders': orders})

@login_required
def order_list_user_self(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set')
    return render(request, 'order_list_user_self.html', {'orders': orders})

@login_required
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'user_reviews.html', {'reviews': reviews})


def wish_list(request):
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.user = request.user
            wish.save()
            return redirect('wish_list')
    else:
        form = WishForm()

    wishes = Wish.objects.all()
    return render(request, 'wish_list.html', {'form': form, 'wishes': wishes})

@login_required
def wish_like(request):
    if request.method == 'POST':
        wish_id = request.POST.get('id')
        wish = get_object_or_404(Wish, id=wish_id)

        # Проверяем, проголосовал ли пользователь ранее
        vote, created = Vote.objects.get_or_create(user=request.user, wish=wish, defaults={'vote_type': 'like'})
        
        if not created: 
            if vote.vote_type == 'like':
                vote.delete()
                wish.likes -= 1
            else:
                vote.vote_type = 'like'
                vote.save()
                wish.likes += 1
                wish.dislikes -= 1
        else:  # Новый голос
            wish.likes += 1

        wish.save()
        return JsonResponse({'likes': wish.likes, 'dislikes': wish.dislikes})

@login_required
def wish_dislike(request):
    if request.method == 'POST':
        wish_id = request.POST.get('id')
        wish = get_object_or_404(Wish, id=wish_id)

        vote, created = Vote.objects.get_or_create(user=request.user, wish=wish, defaults={'vote_type': 'dislike'})
        
        if not created:  
            if vote.vote_type == 'dislike':
                vote.delete()
                wish.dislikes -= 1
            else:
                vote.vote_type = 'dislike'
                vote.save()
                wish.dislikes += 1
                wish.likes -= 1
        else:
            wish.dislikes += 1

        wish.save()
        return JsonResponse({'likes': wish.likes, 'dislikes': wish.dislikes})
    
def search(request):
    products_results = []  
    searched = ''  
    if request.method == "POST":
        searched = request.POST.get('searched', '').lower().strip() 
        if searched:  
            # Разделяем поисковый запрос на отдельные слова
            search_terms = re.findall(r'(?i)\b\w+\b', searched)  # findall для извлечения слов
            queries = Q()
            for term in search_terms:
                queries |= (
                    Q(name__icontains=term) |  # Поиск по имени продукта
                    Q(category__name__icontains=term) |  # Поиск по имени категории
                    Q(ingredients__icontains=term) |  # Поиск по ингредиентам
                    Q(description__icontains=term)  # Поиск по описанию
                )
            products_results = Product.objects.filter(queries) 
    context = {
        'searched': searched,
        'products_results': products_results
    }
    return render(request, "search/search_results.html", context=context)


from django import forms
from .models import Order, OrderItem, Decoration, Product, Wish, Review

# Форма Заказа
class OrderForm(forms.ModelForm):
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Товар",
        widget=forms.Select(attrs={'id': 'product-select'}),
    )
    weight = forms.FloatField(required=False, label="Вес (кг)", min_value=1)
    quantity = forms.IntegerField(required=False, label="Количество (шт)", min_value=1)
    decoration = forms.ModelChoiceField(queryset=Decoration.objects.all(), label="Сложность декора")
    wishes = forms.CharField(
        required=False, 
        label="Пожелания по декору",
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 20})
    )
    
    delivery_method = forms.ChoiceField(
        choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')],
        label="Способ доставки"
    )
    delivery_address = forms.CharField(required=False, max_length=255, label="Адрес доставки")

    class Meta:
        model = Order
        fields = ['product', 'decoration', 'wishes', 'delivery_method', 'delivery_address']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['product'].label_from_instance = lambda obj: f"{obj.category}: {obj.name} ({obj.price} руб.)"

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        
        if product and product.category == 'Торты':
            self.fields['quantity'].widget.attrs['readonly'] = False  # Разрешаем ввод количества
            self.fields['weight'].widget.attrs.pop('readonly', None)  # Разрешаем ввод веса
        else:
            self.fields['weight'].widget.attrs['readonly'] = 'readonly'  # Блокируем поле веса
            self.fields['quantity'].widget.attrs['readonly'] = False  # Разрешаем ввод количества
        return cleaned_data

# Форма Пожелания о включении продукции
class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ['category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Опишите изделие, которое вы желаете видеть в нашем ассортименте...'}),
        }
        labels = {
            'category': 'Категория',  
            'description': 'Описание изделия',  
        }

# Форма для отправки Отзыва
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Ваш отзыв...', 'rows': 10, 'cols': 40}),
        }
        labels = {
            'text': 'Текст',  
        }

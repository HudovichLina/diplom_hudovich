from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import UserProfile

# Форма регистрации нового пользователя
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(
        max_length=17,
        required=True,
        label='Телефон',
        widget=forms.TextInput(attrs={'id': 'phone_input'})
    )
    date_of_birth = forms.DateField(required=True, label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "date_of_birth", "password1", "password2")
        labels = {
            'first_name': 'Имя',  
            'last_name': 'Фамилия',  
            'password1': 'Пароль',  
            'password2': 'Повторите пароль',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone):
            raise ValidationError(_('Неверный формат телефона. Используйте: +375(29)___-__-__.'))
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Пользователь с таким email уже существует.'))
        return email
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = user.userprofile 
            user_profile.phone_number = self.cleaned_data.get('phone')
            user_profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            user_profile.save()
        return user

# Форма изменения данных пользователя
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Пользователь с таким email уже существует.'))
        return email

# Форма изменения профиля пользователя
class ProfileEditForm(forms.ModelForm):
 
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'phone_number')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError(_('Неверный формат телефона. Используйте: +375(29)___-__-__.'))
        return phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone_number')
        email = self.instance.user.email

        if UserProfile.objects.exclude(user=self.instance.user).filter(phone_number=phone).exists():
            self.add_error('phone_number', 'Пользователь с таким номером телефона уже существует.')



            
from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone_number')  # Поля для отображения
    # search_fields = ('user', 'phone_number')  # Поля для поиска

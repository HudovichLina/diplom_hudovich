from django.urls import path, re_path, include
from .views import register_view,  profile_edit 

urlpatterns = [
    re_path(r'^register/', register_view, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile_edit, name='user_profile'),
]

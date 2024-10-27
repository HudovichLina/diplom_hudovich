from django.urls import path, re_path
from .views import StartBotView

urlpatterns = [
    path('start-bot/', StartBotView.as_view(), name='start-bot'),  
]

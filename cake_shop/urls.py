from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AboutView, ContactView

urlpatterns = [
        path('admin/', admin.site.urls),
        path('catalog/', include('catalog.urls')),
        path('account/', include('account.urls')),
         path('bot/', include('telegram_bot.urls')),
        path('about/', AboutView.as_view(), name='about'),
        path('contacts/', ContactView.as_view(), name='contacts'),
        path('dreamtaste', views.home_page, name='home_page'),  
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

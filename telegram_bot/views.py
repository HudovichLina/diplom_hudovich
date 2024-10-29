
from django.http import JsonResponse

from .telegram_bot import main
from django.views import View
import re
import asyncio

class StartBotView(View):
    async def get(self, request):
        asyncio.create_task(main()) 
        return JsonResponse({'status': 'Бот запущен'})
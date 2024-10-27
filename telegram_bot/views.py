
from django.http import JsonResponse

from .telegram_bot import main
from django.views import View
import re
import asyncio

class StartBotView(View):
    async def get(self, request):
        # Запустите бота асинхронно
        asyncio.create_task(main())  # Используем create_task для запуска асинхронной функции
        return JsonResponse({'status': 'Бот запущен'})
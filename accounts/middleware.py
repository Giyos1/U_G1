import time

from django.http import HttpResponse
from django.utils import timezone


class LoggIPWriterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        now = timezone.now()

        ip = request.META.get('REMOTE_ADDR', 'ip addres nomalum')

        print(f'{[now]} ip address {ip}')

        return self.get_response(request)


class LoggUserAgentWriterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        now = timezone.now()

        if now.hour < 8 or now.hour > 18:
            return HttpResponse('Saytimiz 8:00 dan 18:00 gachja ishlaydi')
        return self.get_response(request)


class BlockIPMiddleware:
    requests = {}
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'Noma’lum IP')

        now = time.time()
        if ip not in self.requests:
            self.requests[ip] = []

        # 10 soniyadan eski so‘rovlarni o‘chirib tashlaymiz
        self.requests[ip] = [t for t in self.requests[ip] if now - t < 10]
        if len(self.requests[ip]) >= 5:
            return HttpResponse(
                "Siz 10 soniya ichida juda ko‘p so‘rov yubordingiz. Keyinroq urinib ko‘ring.")

        self.requests[ip].append(now)

        return self.get_response(request)

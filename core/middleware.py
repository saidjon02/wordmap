from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user mavjudligini tekshirish kerak
        if hasattr(request, 'user'):
            user = request.user
            # user bilan ishlash
        else:
            user = None

        response = self.get_response(request)
        return response

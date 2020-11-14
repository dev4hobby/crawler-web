from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings
from module.crawler import Naver
from weather.models import WeatherInfo
import json

naver = Naver()

@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):

    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status=status)

class WeatherSearchView(BaseView):

    def post(self, request):
        location = request.POST.get('location')
        response = naver.get_weather(location)
        if response.get('data'):
            try:
                WeatherInfo.objects.create(location=response.get('data')[0],
                                    temperature=response.get('data')[1],
                                    difference=response.get('data')[2])
            except Exception as e:
                response = None
        return self.response(data = {'weather_info' : response.get('data')},
                             message = response.get('data') and 'Okay' or 'Fail',
                             status = response.get('status'))

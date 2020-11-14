from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings
from module.crawler import Naver
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
        return self.response(data = {'weather_info' : response.get('data')},
                             message = response.get('data') and 'Okay' or 'Fail',
                             status = response.get('status'))

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from ..utils import crypto

class BaseController():
    
    def __init__(self):
        self.invalidJson = {"Error": "Invalid json body"}

    def bodyParser(self, body):
        bodyDecode = body.decode('utf-8')
        try:
            content = json.loads(bodyDecode)
        except json.JSONDecodeError:
            return False
        return content

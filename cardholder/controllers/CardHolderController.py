from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from ..dbmodel.CardHolderModel import CardHolderModel
from django.views.decorators.csrf import csrf_exempt
from ..utils import crypto
from django.core.exceptions import ObjectDoesNotExist
from .BaseController import BaseController
import re
import json

class CardHolderController(BaseController):

    def __init__(self):
        super().__init__()

    @csrf_exempt
    def create(self, request):
        if request.method == 'POST':
            content = self.bodyParser(request.body)
            if content == False:
                return JsonResponse(self.invalidJson, status=400)

            validator = self.createValidator(content)
            if validator != True:
                return JsonResponse(validator, status=400)

            email = content['email']
            cardNo = content['card_number']
            fullName = content['full_name']
            expiryDate = content['expiry_date']
            ccv = content['ccv']

            cardObj = {
                "full_name": fullName,
                "expiry_date": expiryDate,
                "card_number": cardNo,
                "ccv": ccv
            }

            token = crypto.encrypt(cardObj)
            publicKey = crypto.publicKeyGenerator()

            try:
                instance = CardHolderModel(
                    token=token,
                    public_key=publicKey
                )

                instance.save()
            except Exception as err:
                response = {"Error": "An error occurs"}
                return JsonResponse(response, status=400)

            success = {
                "email": email,
                "public_key": publicKey
            }

            return JsonResponse(success, status = 201)
        else:
            return HttpResponseBadRequest()

    @csrf_exempt
    def delete(self, request):
        if request.method == 'DELETE':
            content = self.bodyParser(request.body)
            if content == False:
                return JsonResponse(self.invalidJson, status=400)

            publicKey = content['public_key']

            try:
                instance = CardHolderModel.objects.get(public_key=publicKey)
            except ObjectDoesNotExist as err:
                response = {"Error": "Public key does not match any record"}
                return JsonResponse(response, status=404)

            instance.delete()
            success = {"response": "Record is deleted successfully!"}
            return JsonResponse(success, status = 200)
        else:
            return HttpResponseBadRequest()

    def createValidator(self, content):
        if "email" not in content:
            return {"Error": "Email can not be empty!"}

        if "card_number" not in content:
            return {"Error": "Card number can not be empty!"}

        if "full_name" not in content:
            return {"Error": "Card holder name can not be empty"}

        if "expiry_date" not in content:
            return {"Error": "Expiry date can not be empty"}

        if "ccv" not in content:
            return {"Error": "CCV can not be empty"}

        if len(str(content["ccv"])) != 3:
            return {"Error": "Invalid CCV"}

        expiryDatePattern = re.compile("[0-1][1-2][/][0-9][0-9]")
        
        if not expiryDatePattern.match(content["expiry_date"]):
            return {"Error": "Expiry date is in wrong format"}

        if len(str(content["card_number"])) != 16:
            return {"Error": "Invalid card number!"}

        return True

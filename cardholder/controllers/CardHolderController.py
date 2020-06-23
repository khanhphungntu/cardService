from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from ..dbmodel.CardHolderModel import CardHolderModel
from ..serializer.CardHolderSerializer import CardHolderSerializer
from .VisaAPIController import VisaAPIController
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from ..utils import crypto
from django.core.exceptions import ObjectDoesNotExist
from .BaseController import BaseController
import re
import json


class CardHolderListController(BaseController, APIView):

    def __init__(self):
        super().__init__()
        self.visaAPIController = VisaAPIController()

    def post(self, request):

        content = request.data
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

        validateCard = self.visaAPIController.accountValidation(cardObj)
        if validateCard != True:
            return JsonResponse(validateCard, status=400)

        token = crypto.encrypt(cardObj)
        publicKey = crypto.publicKeyGenerator()

        try:
            instance = {
                "token": token,
                "public_key": publicKey
            }

            serializer = CardHolderSerializer(data=instance)
            serializer.is_valid(True)
            serializer.save()
        except Exception as err:
            response = {"Error": "An error occurs"}
            return JsonResponse(response, status=400)

        success = {
            "email": email,
            "public_key": publicKey
        }

        return JsonResponse(success, status=201)

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

        expiryDatePattern = "[0-1][0-2][/][0-9][0-9]"

        if not re.findall(expiryDatePattern, content["expiry_date"]):
            return {"Error": "Expiry date is in wrong format"}

        if len(str(content["card_number"])) != 16:
            return {"Error": "Invalid card number!"}

        return True


class CardHolderDetailController(BaseController, APIView):
    def __init__(self):
        super().__init__()

    def get(self, request, publicKey):
        try:
            instance = CardHolderModel.objects.get(public_key=publicKey)
        except ObjectDoesNotExist as err:
            response = {"Error": "Public key does not match any record"}
            return JsonResponse(response, status=404)

        cardDetails = crypto.decrypt(instance.token)
        response = {
            "public_key": instance.public_key,
            "card_details": cardDetails
        }
        return JsonResponse(response, status=200)

    def delete(self, request, publicKey):
        try:
            instance = CardHolderModel.objects.get(public_key=publicKey)
        except ObjectDoesNotExist as err:
            response = {"Error": "Public key does not match any record"}
            return JsonResponse(response, status=404)

        instance.delete()
        success = {"response": "Record is deleted successfully!"}
        return JsonResponse(success, status=200)

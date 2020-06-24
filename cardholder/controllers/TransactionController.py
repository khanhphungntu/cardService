from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from ..dbmodel.CardHolderModel import CardHolderModel
from .VisaAPIController import VisaAPIController
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from ..utils import crypto
import json


class TransactionController(APIView):

    def __init__(self):
        self.visaAPIController = VisaAPIController()

    def post(self, request):

        content = request.data
        senderKey = content['sender_key']
        recipientKey = content['recipient_key']
        amount = content['amount']
        currency = content['currency']

        try:
            senderInstance = CardHolderModel.objects.get(public_key=senderKey)
            recipientInstance = CardHolderModel.objects.get(
                public_key=recipientKey)
        except ObjectDoesNotExist as err:
            response = {"Error": "Public key does not match any record"}
            return JsonResponse(response, status=404)

        senderCard = crypto.decrypt(senderInstance.token)
        recipientCard = crypto.decrypt(recipientInstance.token)

        response = self.visaAPIController.pushTransaction(
            senderCard, recipientCard, amount, currency)

        if response["status"] == True:
            success = {"response": "Money is transfered successfully!",
                       "transactionIdentifier": response["transactionIdentifier"]}
            return JsonResponse(success)
        else:
            fail = {"Error": response["Error"]}
            return JsonResponse(fail, status=404)

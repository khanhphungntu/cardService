import json
import re
import requests
from django.conf import settings
from datetime import datetime
from ..utils import crypto

class VisaAPIController():

    def __init__(self):
        self.caPath = settings.VISACA
        self.keyPath = settings.VISAKEY
        self.certPath = settings.VISACERT
        self.userId = settings.VISAUSERID
        self.password = settings.VISAPWD

    def accountValidation(self, creditCard: dict):
        validator = self.cardValidator(creditCard)
        if validator != True:
            return validator

        expiryDate = creditCard['expiry_date'].split('/')
        year = "20" + expiryDate[1]
        month = expiryDate[0]

        body = {
            "cardExpiryDate": year + "-" + month,
            "cardCvv2Value": creditCard['ccv'],
            "primaryAccountNumber": creditCard['card_number']
        }

        response = requests.post("https://sandbox.api.visa.com/pav/v1/cardvalidation",
                                 verify=self.caPath,
                                 cert=(self.certPath, self.keyPath),
                                 headers={"Accept": "application/json",
                                          'Content-Type': 'application/json'},
                                 auth=(self.userId, self.password),
                                 data=json.dumps(body))

        if response.status_code == 200:
            content = json.loads(response.text)
            if content["actionCode"] == "00":
                return True
            else:
                return {"Error": "Invalid card details"}

        content = json.loads(response.text)
        return {"Error": content["errorMessage"]}

    def cardValidator(self, creditCard: dict):
        if "card_number" not in creditCard:
            return {"status": False, "Error": "Card number can not be empty!"}

        if "full_name" not in creditCard:
            return {"status": False, "Error": "Card holder name can not be empty"}

        if "expiry_date" not in creditCard:
            return {"status": False, "Error": "Expiry date can not be empty"}

        if "ccv" not in creditCard:
            return {"status": False, "Error": "CCV can not be empty"}

        if len(str(creditCard["ccv"])) != 3:
            return {"status": False, "Error": "Invalid CCV"}

        expiryDatePattern = "[0-1][0-2][/][0-9][0-9]"

        if not re.findall(expiryDatePattern, creditCard["expiry_date"]):
            return {"status": False, "Error": "Expiry date is in wrong format"}

        if len(str(creditCard["card_number"])) != 16:
            return {"status": False, "Error": "Invalid card number!"}

        return True

    def pushTransaction(self, senderCard: dict, recipientCard: dict, amount: str, currency: str):
        senderValidator = self.cardValidator(senderCard)

        if senderValidator != True:
            return senderValidator

        receipientValidator = self.cardValidator(recipientCard)

        if receipientValidator != True:
            return receipientValidator

        try: 
            float(amount)
        except ValueError:
            return {"status": False, "Error": "Invalid amount input!"}

        currentTime = datetime.now().isoformat()
        body = {
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "amount": str(amount),
            "businessApplicationId": "AA",
            "cardAcceptor": {
                "address": {
                    "country": "USA",
                    "state": "CA",
                    "zipCode": "94404"
                },
                "idCode": "CA-IDCode-77765",
                "name": "Acceptor 1",
                "terminalId": "TID-9999"
            },
            "localTransactionDateTime": currentTime,
            "recipientPrimaryAccountNumber": recipientCard["card_number"],
            "recipientName": recipientCard["full_name"],
            "retrievalReferenceNumber": "330000550000",
            "senderAccountNumber": senderCard["card_number"],
            "senderName": senderCard["full_name"],
            "sourceOfFundsCode": "05",
            "systemsTraceAuditNumber": "451000",
            "transactionCurrencyCode": currency
        }

        response = requests.post("https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions",
                            verify=self.caPath,
                            cert=(self.certPath, self.keyPath),
                            headers={"Accept": "application/json",
                                    'Content-Type': 'application/json'},
                            auth=(self.userId, self.password),
                            data=json.dumps(body))

        if response.status_code == 200:
            content = json.loads(response.text)
            print(content)
            if content["actionCode"] == "00":
                return {"status": True, "transactionIdentifier": content["transactionIdentifier"]}
            else:
                return {"status": False, "Error": "Card can not perform transaction"}
        
        content = json.loads(response.text)
        return {"status": False, "Error": content["errorMessage"]}
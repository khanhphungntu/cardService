import json
import re
import requests
from django.conf import settings


class VisaAPIController():

    def accountValidation(self, creditCard):
        validator = self.cardValidator(creditCard)
        if validator != True:
            return validator

        caPath = settings.VISACA
        keyPath = settings.VISAKEY
        certPath = settings.VISACERT
        userId = settings.VISAUSERID
        password = settings.VISAPWD

        expiryDate = creditCard['expiry_date'].split('/')
        year = "20" + expiryDate[1]
        month = expiryDate[0]

        body = {
            "cardExpiryDate": year + "-" + month,
            "cardCvv2Value": creditCard['ccv'],
            "primaryAccountNumber": creditCard['card_number']
        }

        response = requests.post("https://sandbox.api.visa.com/pav/v1/cardvalidation",
                                 verify=caPath,
                                 cert=(certPath, keyPath),
                                 headers={"Accept": "application/json",
                                          'Content-Type': 'application/json'},
                                 auth=(userId, password),
                                 data=json.dumps(body))

        if response.status_code == 200:
            content = json.loads(response.text)
            if content["actionCode"] == "00":
                return True
            else:
                return {"Error": "Invalid card details"}

        content = json.loads(response.text)
        return {"Error": content["errorMessage"]}

    def cardValidator(self, creditCard):
        if "card_number" not in creditCard:
            return {"Error": "Card number can not be empty!"}

        if "full_name" not in creditCard:
            return {"Error": "Card holder name can not be empty"}

        if "expiry_date" not in creditCard:
            return {"Error": "Expiry date can not be empty"}

        if "ccv" not in creditCard:
            return {"Error": "CCV can not be empty"}

        if len(str(creditCard["ccv"])) != 3:
            return {"Error": "Invalid CCV"}

        expiryDatePattern = "[0-1][0-2][/][0-9][0-9]"

        if not re.findall(expiryDatePattern, creditCard["expiry_date"]):
            return {"Error": "Expiry date is in wrong format"}

        if len(str(creditCard["card_number"])) != 16:
            return {"Error": "Invalid card number!"}

        return True

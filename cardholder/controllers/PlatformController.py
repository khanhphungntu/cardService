# from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
# from ..dbmodel.PlatformModel import PlatformModel
# from django.views.decorators.csrf import csrf_exempt
# import json
# from ..utils import crypto
# from django.contrib.auth.hashers import make_password, check_password
# from django.db import IntegrityError
# from django.core.exceptions import ObjectDoesNotExist


# class PlatformController():

#     @csrf_exempt
#     def create(request):
#         if request.method == 'POST':
#             body = request.body.decode('utf-8')
#             platform = json.loads(body)
#             email = platform['email']
#             password = make_password(platform['password'])
#             name = platform['name']
#             publicKey = crypto.publicKeyGenerator()
#             privateKey = crypto.privateKeyGenerator()

#             try:
#                 instance = PlatformModel(
#                     email=email,
#                     password=password,
#                     name=name,
#                     public_key=publicKey,
#                     private_key=privateKey
#                 )

#                 instance.save()
#             except IntegrityError as err:
#                 response = {"Error": "Email has already been registered"}
#                 return JsonResponse(response, status=400)

#             success = {"Success": "Account is created successfully!"}
#             return JsonResponse(success)
#         else:
#             return HttpResponseBadRequest()

#     @csrf_exempt
#     def getPublicKey(request):
#         if request.method == 'POST':
#             body = request.body.decode('utf-8')
#             authentication = json.loads(body)
#             email = authentication['email']
#             password = authentication['password']

#             try:
#                 platform = PlatformModel.objects.get(email=email)
#             except ObjectDoesNotExist as err:
#                 response = {"Error": "User has not registered!"}
#                 return JsonResponse(response, status=400)

#             if check_password(password, platform.password):
#                 response = {"public_key": platform.public_key}
#             else:
#                 response = {"Error": "Incorrect password"}

#             return JsonResponse(response)
#         else:
#             return HttpResponseBadRequest()

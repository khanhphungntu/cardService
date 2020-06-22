from django.urls import path
from . import views
from .controllers.CardHolderController import CardHolderListController, CardHolderDetailController

cardHolderListController = CardHolderListController()
cardHolderDetailController = CardHolderDetailController()

urlpatterns = [
    path('card', cardHolderListController.as_view(), name='CardList'),
    path('card/<str:publicKey>', cardHolderDetailController.as_view(), name="CardDetail")
]

from django.urls import path
from . import views
from .controllers.CardHolderController import CardHolderListController, CardHolderDetailController
from .controllers.TransactionController import TransactionController

cardHolderListController = CardHolderListController()
cardHolderDetailController = CardHolderDetailController()
transactionController = TransactionController()

urlpatterns = [
    path('card', cardHolderListController.as_view(), name='CardList'),
    path('card/<str:publicKey>', cardHolderDetailController.as_view(), name="CardDetail"),
    path('transaction', transactionController.as_view(), name="transaction")
]

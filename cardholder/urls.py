from django.urls import path
from . import views
from .controllers.CardHolderController import CardHolderController

cardHolderController = CardHolderController()

urlpatterns = [
    path('card/add', cardHolderController.create, name='addCard'),
    path('card/delete', cardHolderController.delete, name='deleteCard'),
]

from django.contrib import admin

# Register your models here.
from .dbmodel.CardHolderModel import CardHolderModel

class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_key', 'token')

admin.site.register(CardHolderModel, CardHolderAdmin)
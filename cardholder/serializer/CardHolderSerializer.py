from rest_framework import serializers
from ..dbmodel.CardHolderModel import CardHolderModel

class CardHolderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    token = serializers.CharField(max_length=255)
    public_key = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(required = False)

    def create(self, validated_data):
        """
        Create and return a new `Card` instance, given the validated data.
        """
        return CardHolderModel.objects.create(**validated_data)

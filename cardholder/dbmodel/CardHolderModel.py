from django.db import models

class CardHolderModel(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.id) + "_" + self.public_key

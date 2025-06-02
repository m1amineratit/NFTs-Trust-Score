from django.db import models

# Create your models here.


class Wallet(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class Score(models.Model):
    score = models.IntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    note = models.CharField(max_length=250)
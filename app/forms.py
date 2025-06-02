from django import forms 
from .models import Wallet, Score


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('name',)

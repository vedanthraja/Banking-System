from django import forms
from .models import customer, account, trans_info

class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = '__all__'

class PinForm(forms.ModelForm):
    class Meta:
        model = account
        fields = ('pin',)

class LoginForm(forms.ModelForm):

    class Meta:
        model = account
        fields = ('acct_no', 'pin')

class TransactionForm(forms.Form):
    amt = forms.DecimalField(label = 'Amount', max_digits = 12, decimal_places = 2)
    credit_acct_no = forms.CharField(label = 'Credit Account Number', max_length = 13)
    pin = forms.CharField(label = 'Account Pin',max_length = 6, widget = forms.PasswordInput())
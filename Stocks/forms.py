from django import forms


# Stock ticker form
class StockTickerForm(forms.Form):
    ticker = forms.CharField(label='', max_length=5, required=True)
    # Django forms do not include <form> tag or submit button, we have to add them ourselves in the template


# User form for sign up
class SignUpForm(forms.Form):
    fullName = forms.CharField(label='', max_length=30, required=True)
    email = forms.EmailField(label='', required=True)
    username = forms.CharField(label='', max_length=15, required=True)
    password = forms.CharField(label='', max_length=20, required=True)

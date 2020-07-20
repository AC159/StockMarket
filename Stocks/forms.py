from django import forms


# Stock ticker form
class StockTickerForm(forms.Form):
    ticker = forms.CharField(label='', max_length=5, required=True)
    # Django forms do not include <form> tag or submit button, we have to add them ourselves in the template

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
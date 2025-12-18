from django import forms
from .models import Review

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text_review']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Ваше імʼя"}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text_review': forms.Textarea(attrs={'rows': 4, 'placeholder': "Ваш відгук"}),
        }
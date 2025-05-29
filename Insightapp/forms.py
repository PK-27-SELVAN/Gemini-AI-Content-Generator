from django import forms
from .models import SearchHistory

class Searchform(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = ['search_text']
        labels = {
            'search_text': ''  # This removes the label
        }
        widgets = {
            'search_text':forms.TextInput(attrs={'placeholder':'Enter your Query Here....'})
        }
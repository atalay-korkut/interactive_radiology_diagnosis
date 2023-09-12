from django import forms
from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('title', 'image', 'clicks', 'outputText', 'inputText')

    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)
        self.fields['clicks'].required = False
        self.fields['outputText'].required = False
        self.fields['inputText'].required = False
        self.fields['clicks'].widget = forms.HiddenInput()
        self.fields['outputText'].widget = forms.HiddenInput()
        self.fields['inputText'].widget = forms.HiddenInput()

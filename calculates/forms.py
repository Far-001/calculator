from django import forms

class CalcForm(forms.Form):
    expression = forms.CharField(max_length=100)
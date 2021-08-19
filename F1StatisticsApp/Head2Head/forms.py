from django.forms import ModelForm
from  django import forms
from django.forms.widgets import DateInput

class Driverform(forms.Form):
    driver1 = forms.CharField(label='Enter first Driver', max_length=100)
    driver2 = forms.CharField(label='Enter second Driver', max_length=100)
    
class Teamform(forms.Form):
    team1 = forms.CharField(label='Enter first Team', max_length=100)
    team2 = forms.CharField(label='Enter second Team', max_length=100)

class DeleteSpecificForm(forms.Form):
    gp = forms.CharField(label='Enter GrandPrix', max_length=100)
    sess = forms.CharField(label='Enter GrandPrix', max_length=100)
    pw = forms.CharField(label='Enter Password', max_length=100)

class CheckForm(forms.Form):
    pw = forms.CharField(label='Enter Password', max_length=100)
from django import forms 

class NewGroupForm(forms.Form):


    nazwa= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwa'}))
    opis = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Opis'}))


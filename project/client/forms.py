from django import forms 

AVATARS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        
    ]
class SettingsForms(forms.Form):


    name = forms.CharField(label="Imię",required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    surname = forms.CharField(label="Nazwisko",required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))
    address = forms.CharField(label="Adres",required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres'}))
    description = forms.CharField(label="Opis",required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Opis'}))
    avatars = forms.ChoiceField(required=False,
        choices=AVATARS, 
        widget=forms.RadioSelect(attrs={'class':'d-inline'})
    )

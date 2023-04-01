from django import forms


from cafedra.models import Cafedra, CafedraManager

class CafedraForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Kafedra nomi',
        'type': 'text',
    }))

    faculty = forms.Select()
    
    class Meta:
        model = Cafedra
        fields = ['name']
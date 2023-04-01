

from django import forms

from study_plan.models import Direction, SmallGroup

class DirectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ''' Yo'nalish nomi '''}))
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ''' Yo'nalish kodi '''}))
    semester_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    language = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select rounded-0'},),
        choices=Direction.LANGUAGE_CHOICES,
    )

    study_form = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select rounded-0'},),
        choices=Direction.STUDY_FORM_CHOICES,
    )

    class Meta:
        model = Direction
        fields = [ 'name', 'language', 'study_form', 'code', 'semester_number']


class SmallGroupForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={ 'class': 'form-control' }
    ))

    class Meta:
        model = SmallGroup
        fields = ['name', 'direction']

    def __init__(self, faculty = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direction'].widget.attrs.update({'class': 'custom-select rounded-0'})
        if faculty is not None:
            self.fields['direction'].queryset = Direction.objects.filter(faculty__id=faculty.pk).all()



class CustomTextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control'})
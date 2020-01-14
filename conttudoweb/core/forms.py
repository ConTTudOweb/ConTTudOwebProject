from django import forms

from conttudoweb.core.models import People


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'
        widgets = {
            'observation': forms.Textarea(attrs={'rows': 3})
        }

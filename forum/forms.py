from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Rent, Comment


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ['owner', 'occupant', 'date_posted', 'is_closed']
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.helper = FormHelper()
    #     self.helper.form_method = 'POST'
    #     self.helper.add_input(Submit('submit', 'Simpan'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'rent']


class ConfirmationForm(forms.Form):
    confirm = forms.BooleanField(label="Saya yakin dan bersedia mengikuti aturan yang berlaku")



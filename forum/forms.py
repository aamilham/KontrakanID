from django import forms

from .models import Rent, Comment


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ['owner', 'occupant', 'date_posted', 'is_closed']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'rent']



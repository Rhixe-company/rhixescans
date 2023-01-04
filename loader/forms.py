from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Comics.models import *


class ComicSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Genre.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'Genre'
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username',
                  'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ComicForm(ModelForm):
    class Meta:
        model = Comic
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'genres': forms.CheckboxSelectMultiple(),
        }


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = ['user']
        widgets = {
            'pages': forms.CheckboxSelectMultiple(),
        }


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = "__all__"


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']

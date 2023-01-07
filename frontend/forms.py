from django.forms import ModelForm

from django import forms
from Comics.models import *




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

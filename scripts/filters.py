import django_filters
from django_filters import CharFilter

from django import forms

from .models import *


class ComicFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr="icontains", label='Title')

    class Meta:
        model = Comic
        fields = ['title']

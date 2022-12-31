import django_filters
from django_filters import CharFilter

from django import forms

from Comics.models import *


class ComicsFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr="icontains", label='Title')
    genres = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple
                                                      )

    class Meta:
        model = Comic
        fields = ['title', 'genres']

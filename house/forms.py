from django import forms

from house.models import House


class SearchForm(forms.ModelForm):
    region_field = forms.CharField(label='Region', widget=forms.TextInput())
    city_field = forms.CharField(label='City', widget=forms.TextInput())

    class Meta:
        model = House
        fields = ('region_field', 'city_field', 'street', 'number')


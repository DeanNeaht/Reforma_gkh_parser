from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from house.forms import SearchForm
from house.models import House, Region, City
from house.services.analysis import house_analysis


class SearchFormView(CreateView):
    """
    House search page view
    """
    model = House
    template_name = 'search.html'
    form_class = SearchForm
    success_url = reverse_lazy('search')

    def form_valid(self, form):
        data = form.cleaned_data
        form.instance.region = Region.objects.get_or_create(region_name=data.get('region_field').capitalize())[0]
        form.instance.city = City.objects.get_or_create(city_name=data.get('city_field').capitalize())[0]
        return super().form_valid(form)


class AllHousesView(ListView):
    """
    Page with a list of all found houses
    """
    model = House
    template_name = 'all_houses.html'
    paginate_by = 20

    def get_queryset(self):
        return House.objects.all().select_related('city', 'region',
                                                  'load_bearing_wall_material').filter(is_find=True)


class AllTheRestView(View):
    """
    Page with analysis of found houses
    """

    def get(self, request):
        count_found, count_bricks, max_floor = house_analysis()
        return render(request, template_name='all_the_rest.html', context={'count_found': count_found,
                                                                           'count_bricks': count_bricks,
                                                                           'max_floors': max_floor})

from django.urls import path

from house.views import SearchFormView, AllHousesView, AllTheRestView

urlpatterns = [
    path('', SearchFormView.as_view(), name='search'),
    path('all_houses', AllHousesView.as_view(), name='all_houses'),
    path('all_the_rest', AllTheRestView.as_view(), name='all_the_rest'),
]
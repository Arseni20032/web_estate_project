from django_filters import rest_framework as filters

from ..models import Estate


class EstateFilter(filters.FilterSet):
    min_cost = filters.NumberFilter(field_name="cost", lookup_expr='gte')
    max_cost = filters.NumberFilter(field_name="cost", lookup_expr='lte')
    # estate_type = filters.

    class Meta:
        model = Estate
        fields = ['cost', 'estate_type']

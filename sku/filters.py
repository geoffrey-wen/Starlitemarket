import django_filters
from .models import Product, Inbound, SKU, Warehouse, Marketplace
from django_filters import CharFilter

class SkuProductFilter(django_filters.FilterSet):
    location = CharFilter(field_name='location__slug', lookup_expr='icontains')
    inbound_order = CharFilter(field_name='inbound_order__code', lookup_expr='icontains')
    outbound_order = CharFilter(field_name='out_order__code', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
       super(SkuProductFilter, self).__init__(*args, **kwargs)
       self.filters['location'].label="Location"
       self.filters['inbound_order'].label = "Inbound Order"
       self.filters['outbound_order'].label = "Outbound Order"
       self.filters['note'].label="Note"

class WarehouseProductFilter(django_filters.FilterSet):
    sku = CharFilter(field_name='sku__slug', lookup_expr='icontains')
    inbound_order = CharFilter(field_name='inbound_order__code', lookup_expr='icontains')
    outbound_order = CharFilter(field_name='out_order__code', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
       super(WarehouseProductFilter, self).__init__(*args, **kwargs)
       self.filters['sku'].label="SKU"
       self.filters['inbound_order'].label = "Inbound Order"
       self.filters['outbound_order'].label = "Outbound Order"
       self.filters['note'].label="Note"

class MarketplaceInboundtFilter(django_filters.FilterSet):
    code= CharFilter(field_name='code', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Inbound
        fields = []

    def __init__(self, *args, **kwargs):
       super(MarketplaceInboundtFilter, self).__init__(*args, **kwargs)
       self.filters['code'].label="Code"
       self.filters['note'].label="Note"

class SkuFilter(django_filters.FilterSet):
    slug = CharFilter(field_name='slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = SKU
        fields = []

    def __init__(self, *args, **kwargs):
       super(SkuFilter, self).__init__(*args, **kwargs)
       self.filters['slug'].label = "SKU"
       self.filters['name'].label= "Name"
       self.filters['note'].label= "Note"

class WarehouseFilter(django_filters.FilterSet):
    slug = CharFilter(field_name='slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Warehouse
        fields = []

    def __init__(self, *args, **kwargs):
       super(WarehouseFilter, self).__init__(*args, **kwargs)
       self.filters['slug'].label = "Warehouse"
       self.filters['name'].label= "Name"
       self.filters['note'].label= "Note"

class MarketplaceFilter(django_filters.FilterSet):
    slug = CharFilter(field_name='slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Marketplace
        fields = []

    def __init__(self, *args, **kwargs):
       super(MarketplaceFilter, self).__init__(*args, **kwargs)
       self.filters['slug'].label = "Marketplace"
       self.filters['name'].label= "Name"
       self.filters['note'].label= "Note"
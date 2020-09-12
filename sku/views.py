from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from .models import SKU, Warehouse, Product, TestProduct, Inbound, Outbound, Marketplace
from django.contrib.auth.models import User
from .forms import ProductInboundForm
import json
import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import SkuProductFilter, WarehouseProductFilter, MarketplaceInboundtFilter, SkuFilter, WarehouseFilter, MarketplaceFilter

# Create your views here.
def index(request):
    print(request.user)
    return render(request, 'sku/home.html')

def InboundOrder(request):
    date = datetime.date.today().strftime("%y%m%d")
    serialnumber = '{0:03}'.format(Inbound.objects.filter(date_added__month=datetime.date.today().strftime('%m')).count() + 1)
    code = "IN/"+str(date)+"/"+str(serialnumber)
    if request.method == 'POST':
        tpc = int(request.POST.get('tpc'))
        sku_list = request.POST.getlist("sku[]")
        qty_list = request.POST.getlist("qty[]")
        price_list = request.POST.getlist("price[]")
        tc = sum([int(price_list[i])*int(qty_list[i]) for i in range(len(sku_list))])
        df = tpc/tc
        Inbound.objects.create(
            code = code,
            total_paid_cost =tpc,
            note = str(request.POST.get('note')),
            creator = request.user,
            marketplace = Marketplace.objects.get(pk=request.POST.get('marketplace')),
        )
        print(len(sku_list))
        for i in range(len(sku_list)):
            print(int(qty_list[i]))
            for j in range(int(qty_list[i])):
                Product.objects.create(
                    sku = SKU.objects.get(pk=sku_list[i]),
                    cost = int(price_list[i])*df,
                    inbound_order = Inbound.objects.get(code=code),
                    location = Warehouse.objects.get(slug='in')
                )
        #alert message
        return HttpResponse(json.dumps([]))

    context = {'skus': SKU.objects.all(),
               'marketplaces' : Marketplace.objects.all(),
               'code': code}
    return render(request, "sku/inbound_order.html", context)

def InboundDetail(request, pk):
    inbound = get_object_or_404(Inbound, pk=pk)
    products = Product.objects.filter(inbound_order=inbound)
    locations = Warehouse.objects.all()
    if request.method == 'POST':
        date_list = request.POST.getlist("date[]")
        location_list = request.POST.getlist("location[]")
        note_list = request.POST.getlist("note[]")
        in_note = request.POST.get('in-note')
        inbound.note = in_note
        inbound.save()
        for i in range(products.count()):
            temp = products[i]
            if date_list[i]:
                if products[i].exp_date:
                    temp_date = date_list[i]
                else:
                    temp_date = date_list[i][6:10] + '-' + date_list[i][0:2] + '-' + date_list[i][3:5]
                print(temp_date)
                temp.exp_date = temp_date
            temp.location = Warehouse.objects.get(pk=location_list[i])
            if note_list[i]:
                temp.note = note_list[i]
            temp.save()
        #alert messages
        return HttpResponse(json.dumps([]))

    context = { 'inbound' : inbound,
                'products' : products,
                'locations' : locations}
    return render(request, 'sku/inbound_detail.html', context)

class SkuCreateView(LoginRequiredMixin, CreateView):
    model = SKU
    fields = ['slug', 'name', 'note']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

def SkuList(request):
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    skus = SKU.objects.all()
    sku_count = skus.count()
    sku_filter = SkuFilter(request.GET, queryset=skus)
    skus = sku_filter.qs
    context = {'skus':skus,
               'sku_count':sku_count,
               'sku_filter':sku_filter}
    return render(request, 'sku/sku_list.html', context)

def SkuProductList(request, slug):
    # tambah order by exp date
    # qs sebelum dilembapr ke html dipecah
    # tambah expdate terdekat
    # tambah jumlahstok

    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    sku = get_object_or_404(SKU, slug=slug)
    products = Product.objects.filter(sku=sku)
    product_filter = SkuProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    context = { 'sku' : sku,
                'products' : products,
                'product_filter' : product_filter}
    return render(request, 'sku/sku_detail.html', context)

class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouse
    fields = ['slug', 'name', 'note']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class WarehouseDetailView(LoginRequiredMixin, DetailView):
    model = Warehouse

def WarehouseList(request):
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    warehouses = Warehouse.objects.all()
    warehouse_count = warehouses.count()
    warehouse_filter = WarehouseFilter(request.GET, queryset=warehouses)
    warehouses = warehouse_filter.qs
    context = {'warehouses':warehouses,
               'warehouse_count':warehouse_count,
               'warehouse_filter':warehouse_filter}
    return render(request, 'sku/warehouse_list.html', context)

def WarehouseProductList(request, slug):
    # tambah order by exp date
    # tambah method exp date terdekat
    # tambah jumlahitem
    # tambah value item (totalitemcost)
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    warehouse = get_object_or_404(Warehouse, slug=slug)
    products = Product.objects.filter(location=warehouse)
    product_filter = WarehouseProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    context = { 'warehouse' : warehouse,
                'products' : products,
                'product_filter' : product_filter}
    return render(request, 'sku/warehouse_detail.html', context)

class MarketplaceCreateView(LoginRequiredMixin, CreateView):
    model = Marketplace
    fields = ['slug', 'name', 'note']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class MarketplaceDetailView(LoginRequiredMixin, DetailView):
    model = Marketplace

def MarketplaceList(request):
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    marketplaces = Marketplace.objects.all()
    marketplace_count = marketplaces.count()
    marketplace_filter = MarketplaceFilter(request.GET, queryset=marketplaces)
    marketplaces = marketplace_filter.qs
    context = {'marketplaces':marketplaces,
               'marketplace_count':marketplace_count,
               'marketplace_filter':marketplace_filter}
    return render(request, 'sku/marketplace_list.html', context)

def MarketplaceInboundList(request, slug):
    # tambah totalvaluebelanja
    # tambah percentdiscount
    # tambah jumlahorder
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    marketplace = get_object_or_404(Marketplace, slug=slug)
    inbounds = Inbound.objects.filter(marketplace=marketplace)
    inbound_filter = MarketplaceInboundtFilter(request.GET, queryset=inbounds)
    inbounds = inbound_filter.qs
    context = { 'marketplace' : marketplace,
                'inbounds' : inbounds,
                'inbound_filter' : inbound_filter}
    return render(request, 'sku/marketplace_detail.html', context)

def InboundQualityControl(request):
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    inbounds = Inbound.objects.filter(product__location__slug='in').distinct()
    data = []
    for inbound in inbounds:
        temp = [inbound,
                inbound.product_set.all().count,
                inbound.product_set.exclude(location__slug='in').count,
                inbound.product_set.filter(location__slug='in').count]
        data.append(temp)

    return render(request, 'sku/inbound_qc.html', {'data':data})

def ProductDetail(request, skuslug, expdate):
    if not request.user.username:
        return redirect('/login/?next=%s' % request.path)

    try:
        sku = get_object_or_404(SKU, slug=skuslug)
        date = expdate[6:10] + '-' + expdate[0:2] + '-' + expdate[3:5]
        products = Product.objects.filter(sku = sku, exp_date__date=date)
        locations = Warehouse.objects.all()
    except:
        return redirect('home')

    if request.method=='POST':
        print('sent')
        HttpResponse(json.dumps([]))
        date_list = request.POST.getlist("date[]")
        location_list = request.POST.getlist("location[]")
        note_list = request.POST.getlist("note[]")
        for i in range(products.count()):
            temp = products[i]
            if date_list[i]:
                if products[i].exp_date:
                    temp_date = date_list[i]
                else:
                    temp_date = date_list[i][6:10] + '-' + date_list[i][0:2] + '-' + date_list[i][3:5]
                print(temp_date)
                temp.exp_date = temp_date
            temp.location = Warehouse.objects.get(pk=location_list[i])
            if note_list[i]:
                temp.note = note_list[i]
            temp.save()

    return render(request, 'sku/product_detail.html', {'products':products, 'locations': locations})


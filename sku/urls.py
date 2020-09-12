from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('sku-new', views.SkuCreateView.as_view(), name='sku-create'),
    path('sku/<str:slug>/', views.SkuProductList, name='sku-detail'),
    path('sku-list', views.SkuList, name='sku-list'),

    path('warehouse-new', views.WarehouseCreateView.as_view(), name='warehouse-create'),
    path('warehouse/<str:slug>/', views.WarehouseProductList, name='warehouse-detail'),
    path('warehouse-list', views.WarehouseList, name='warehouse-list'),

    path('marketplace-new', views.MarketplaceCreateView.as_view(), name='marketplace-create'),
    path('marketplace/<str:slug>/', views.MarketplaceInboundList, name='marketplace-detail'),
    path('marketplace-list', views.MarketplaceList, name='marketplace-list'),

    path('in-order', views.InboundOrder, name='inbound-order'),
    path('in/<int:pk>/', views.InboundDetail, name='inbound-detail'),
    path('in-qc', views.InboundQualityControl, name='inbound-qc'),

    path('product/<slug:skuslug>/<str:expdate>', views.ProductDetail, name='product-detail'),
]
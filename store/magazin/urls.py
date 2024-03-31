from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('catalog', catalog),
    path('panel', panel),
    path('cart', cart),
    path('addproduct', add_product),
    path('reg', reg),
    path('auth', auth),
    path('logout', logout),
    path('product/<int:id>', product_id),
    path('order/<int:id>', order_id),
    path('delproduct', del_product),
    path('filter', filter_catalog),
    path('gettotal', gettotal),
    path('order', order),
]

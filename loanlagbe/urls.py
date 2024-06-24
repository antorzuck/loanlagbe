
from django.contrib import admin
from django.urls import path
from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('create-customer', create_customer),
    path('see-customer', show_customer),
    path('add-payment', add_payment)
]

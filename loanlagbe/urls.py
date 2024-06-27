from django.contrib import admin
from django.urls import path
from base.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('create-customer', create_customer),
    path('see-customer', show_customer),
    path('add-payment', add_payment),
    path('profile/<int:id>', view_profile),
    path('loans', loans)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "LoanLagbe Admin"
admin.site.site_title = "LoanLagbe Admin Portal"
admin.site.index_title = "Welcome to LoanLagbe Head Quarter"

from django.contrib import admin
from django.urls import path
from base.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', handle_login),
    path('signin', handle_login),
    path('dashboard', dashboard),
    path('logout', handle_logout),
    path('create-customer', create_customer),
    path('see-customer', show_customer),
    path('add-payment', add_payment),
    path('profile/<int:id>', view_profile),
    path('loans', loans),
    path('edit-profile/<int:customer_id>', edit_profile),
    path('signup', signup),
    path('edit-member', edit_member),
    path('all-member', all_member),
    path('change-password', change_password)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "LoanLagbe Admin"
admin.site.site_title = "LoanLagbe Admin Portal"
admin.site.index_title = "Welcome to LoanLagbe Head Quarter"

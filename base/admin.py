from django.contrib import admin
from base.models import *





admin.site.register([
    Customer,
    Loan,
    Document,
    Payment,
    TotalLoan,
    TotalTake,
    Profile
])

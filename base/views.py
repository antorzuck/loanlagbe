from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone


def dashboard(request):
    today = timezone.now().date()

    loans = TotalLoan.objects.all()
    totalloans = sum([i.amount for i in loans])

    taked = TotalTake.objects.all()
    totaltaked = sum([i.amount for i in taked])

    todayloangive = loans.filter(created_at__date=today)
    print(todayloangive)
    print("hajfhjhfkjhdfjkhsdkjfhsjd")

    context = {
        'totalcustomer' : Customer.objects.all().count(),
        'totalloan' : totalloans,
        'totaltaked' : totaltaked
    }

    return render(request, 'home.html', context)

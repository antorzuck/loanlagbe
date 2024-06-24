from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone


def dashboard(request):
    today = timezone.now().date()

    loans = TotalLoan.objects.all()
    totalloans = sum([i.amount for i in loans])

    taked = TotalTake.objects.all()
    totaltaked = sum([i.amount for i in taked])

    todayloangive = sum([i.amount for i in loans.filter(created_at__date=today)])
    todayloantake = sum([i.amount for i in taked.filter(created_at__date=today)])


    context = {
        'totalcustomer' : Customer.objects.all().count(),
        'totalloan' : totalloans,
        'totaltaked' : totaltaked,
        'todayloangive' : todayloangive,
        'todayloantake' : todayloantake
    }

    return render(request, 'home.html', context)


def create_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        loans_id = request.POST.get('loans')
        total_loan_amount = request.POST.get('total_loan_amount')
        dp = request.FILES.get('dp')
        notes = request.POST.get('notes')
        customer = Customer.objects.create(
            name=name,
            address=address,
            loans=Loan.objects.get(id=loans_id),
            total_loan_amount=total_loan_amount,
            dp=dp,
            notes=notes
        )

        return render(request, 'customer.html', context={'msg' : 'কাস্টমার ক্রিয়েট করা হয়েছে।'})
    context = {
        'loans' : Loan.objects.all()
    }
    return render(request, 'customer.html', context)



def show_customer(request):
    customers = Customer.objects.all()
    if request.GET.get('q'):
        customers = customers.filter(name__icontains=request.GET.get('q'))
    context = {'customer' : customers}
    return render(request, 'seecustomer.html', context)


def add_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        custid = request.POST.get('cid')

        Payment.objects.create(
            customer=Customer.objects.get(id=custid),
            amount=int(amount)
        )
        return redirect('/see-customer')




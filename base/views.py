from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.db.models import Sum
from base.decorators import onlyuser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



def monthly_totals():
    monthly_totals = []
    current_year = timezone.now().year

    for month in range(1, 13):
        monthly_loans = TotalLoan.objects.filter(
            created_at__year=current_year,
            created_at__month=month
        )

        total_amount = monthly_loans.aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_totals.append(total_amount)

    return monthly_totals


@onlyuser
def dashboard(request):
    monthly = monthly_totals()
    today = timezone.now().date()

    loans = TotalLoan.objects.all()
    totalloans = sum([i.amount for i in loans])

    taked = TotalTake.objects.all()
    totaltaked = sum([i.amount for i in taked])

    todayloangive = sum([i.amount for i in loans.filter(created_at__date=today)])
    todayloantake = sum([i.amount for i in taked.filter(created_at__date=today)])

    history = History.objects.all().order_by('-id')[:10]


    context = {
        'totalcustomer' : Customer.objects.all().count(),
        'totalloan' : "{:,}".format(totalloans),
        'totaltaked' : "{:,}".format(totaltaked),
        'todayloangive' : "{:,}".format(todayloangive),
        'todayloantake' : "{:,}".format(todayloantake),
        'monthly' : monthly,
        'history' : history
    }

    return render(request, 'home.html', context)

@onlyuser
def create_customer(request):
    if request.method == 'POST':
        #getting customer text infos
        name = request.POST.get('name')
        loans_id = request.POST.get('loans')
        total_loan_amount = request.POST.get('total_loan_amount')
        mobile = request.POST.get('mobile')
        payable = request.POST.get('payable')

        #getting customer documents info
        cnid = request.FILES.get('cnid')
        cstamp = request.FILES.get('cstamp')
        cphoto = request.FILES.get('cphoto')

        #getting jaminder documents info
        jnid = request.FILES.get('jnid')
        jstamp = request.FILES.get('jstamp')
        jphoto = request.FILES.get('jphoto')
        jname = request.POST.get('jname')


        customer = Customer.objects.create(
            name=name,
            loans=Loan.objects.get(id=loans_id),
            total_loan_amount=total_loan_amount,
         
            mobile=mobile,
            have_to_paid=payable,
            dp=cphoto
        )

        docs = Document.objects.create(
            customer=customer,
            cus_nid=cnid,
            cus_stamp=cstamp,
            cus_photo=cphoto,

            jamin_name=jname,
            jamin_nid = jnid,
            jamin_photo=jphoto,
            jamin_stamp = jstamp
        )

        return render(request, 'customer.html', context={'msg' : 'কাস্টমার ক্রিয়েট করা হয়েছে।', 'loans' : Loan.objects.all()})
    context = {
        'loans' : Loan.objects.all()
    }
    return render(request, 'customer.html', context)


@onlyuser
def show_customer(request):
    customers = Customer.objects.all()
    if request.GET.get('q'):
        customers = customers.filter(name__icontains=request.GET.get('q'))
    context = {'customer' : customers}
    return render(request, 'seecustomer.html', context)

@onlyuser
def add_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        custid = request.POST.get('cid')

        Payment.objects.create(
            customer=Customer.objects.get(id=custid),
            amount=int(amount)
        )
        return redirect('/see-customer')


def view_profile(request, id):
   customer = Customer.objects.get(id=id)
   docs = Document.objects.get(customer=customer)
   context = {'docs':docs, 'profit': abs(customer.profit), 'customer':customer}
   return render(request, 'profile.html', context)

@onlyuser
def loans(request):
    context = { 'loans':Loan.objects.all().order_by('-id')}
    if request.method == 'POST':
        data = request.POST.get('loan_type')
        c = Loan.objects.create(name=data)
        History.objects.create(comment=f"created a loan type {data}")
        return render(request, 'loan.html', context)
    return render(request, 'loan.html', context)




def handle_login(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        ath = authenticate(username=username.strip(), password=password.strip())
        if ath is not None:
            login(request, ath)
            History.objects.create(comment=f"{username} just logged in")
            return redirect(dashboard)
        return render(request, 'login.html', context={'error': 'No user found!'})


@onlyuser
def handle_logout(request):
    logout(request)
    return redirect(handle_login)



from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.db.models import Sum
from base.decorators import onlyuser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def all_member(request):
    users = Profile.objects.all().order_by('-id')
    return render(request, 'all_users.html', {'users': users})



def edit_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    document = get_object_or_404(Document, customer=customer)
    
    if request.method == 'POST':
        # Update Customer info
        customer.name = request.POST.get('name')
        customer.address = request.POST.get('address')
        customer.mobile = request.POST.get('mobile')
        customer.total_loan_amount = request.POST.get('total_loan_amount')
        customer.already_paid = request.POST.get('already_paid')
        customer.have_to_paid = request.POST.get('have_to_paid')
        customer.profit = request.POST.get('profit')

        if 'dp' in request.FILES:
            customer.dp = request.FILES['dp']

        customer.save()

        # Update Document info
        if 'cus_nid' in request.FILES:
            document.cus_nid = request.FILES['cus_nid']
        if 'cus_photo' in request.FILES:
            document.cus_photo = request.FILES['cus_photo']
        if 'cus_stamp' in request.FILES:
            document.cus_stamp = request.FILES['cus_stamp']
        if 'jamin_nid' in request.FILES:
            document.jamin_nid = request.FILES['jamin_nid']
        if 'jamin_photo' in request.FILES:
            document.jamin_photo = request.FILES['jamin_photo']
        if 'jamin_stamp' in request.FILES:
            document.jamin_stamp = request.FILES['jamin_stamp']

        document.jamin_name = request.POST.get('jamin_name')
        document.jamin_mobile = request.POST.get('jamin_mobile')
        document.jamin_address = request.POST.get('jamin_address')

        document.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect(f'/edit-profile/{customer_id}')
    
    context = {
        'customer': customer,
        'document': document,
    }
    return render(request, 'edit.html', context)


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
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
       print("aaaaaaaaaaaaahhhhhhhhhhh", e)
       logout(request)
       return redirect('/')
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
        'profile' : profile,
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
        address = request.POST.get('address')

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
            address=address,
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
            jamin_stamp = jstamp,
            jamin_address = request.POST.get('jaddress'),
            jamin_mobile = request.POST.get('jnum')
        )

        return render(request, 'customer.html', context={'msg' : 'কাস্টমার ক্রিয়েট করা হয়েছে।', 'loans' : Loan.objects.all()})
    context = {
        'loans' : Loan.objects.all()
    }
    return render(request, 'customer.html', context)


@onlyuser
def show_customer(request):
    customers = Customer.objects.all().order_by('-id')
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
            print(ath)
            login(request, ath)
            History.objects.create(comment=f"{username} just logged in")
            return redirect(dashboard)
        return render(request, 'login.html', context={'error': 'No user found!'})


@onlyuser
def handle_logout(request):
    logout(request)
    return redirect(handle_login)


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        dp = request.FILES.get('dp')
        position = request.POST.get('position')
        if " " in username:
            username = username.replace(' ', '')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                profile = Profile(user=user, name=username, address=address, mobile=mobile, dp=dp, position=position)
                profile.save()
                login(request, user)
                return redirect(dashboard)
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'signup.html')




@onlyuser
def edit_member(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        position = request.POST.get('position')
        dp = request.FILES.get('dp')

        if profile:
            profile.name = name
            profile.address = address
            profile.mobile = mobile
            profile.position = position
            if dp:
                profile.dp = dp
            profile.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Profile does not exist')

        return redirect('/edit-member')

    return render(request, 'editmember.html', context={'profile': profile})




@onlyuser
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif old_password == new_password:
            messages.error(request, 'New password cannot be the same as the old password.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/change-password')

    return render(request, 'password.html')



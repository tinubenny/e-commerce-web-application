from django.shortcuts import redirect, render

from customer.models import Customer
from seller.models import Seller
# from .models import Customer
# Create your views here.


def customer_home(request):
    return render(request, 'customer/customer_home.html')


def store(request):
    return render(request, 'customer/store.html')


def product_detail(request):
    return render(request, 'customer/product_detail.html')


def cart(request):
    return render(request, 'customer/cart.html')


def place_order(request):
    return render(request, 'customer/place_order.html')


def order_complete(request):
    return render(request, 'customer/order_complete.html')


def dashboard(request):
    return render(request, 'customer/dashboard.html')


def seller_register(request):
    
    msg = ''
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        city = request.POST['city']
        country = request.POST['country']
        company_name = request.POST['companyName']
        bank_name = request.POST['bankName']
        bank_branch = request.POST['bankBranch']
        account_number = request.POST['accountNumber']
        ifsc = request.POST['ifsc']
        gender = request.POST['gender']
        profile_picture = request.FILES['profilePicture']
        
        
        seller_exist = Seller.objects.filter(email=email).exists()
        
        if not seller_exist:
            seller = Seller(
                first_name = first_name,
                last_name = last_name,
                email = email,
                city = city,
                ifsc_code = ifsc,
                gender = gender,
                country = country,
                company_name = company_name,
                bank_name = bank_name,
                bank_branch = bank_branch,
                account_number = account_number,
                profile_image = profile_picture)
            seller.save()
            msg ='registration successfull'
        else:
            msg ='email already exist'
        
    return render(request, 'customer/seller_register.html',{'status':msg})

def seller_login(request):
    message = ''
    if request.method =="POST":
        username = request.POST['sellerId']
        password = request.POST['password']

        seller = Seller.objects.filter(login_id = username, password = password)
        if seller.exists():
            request.session['seller'] = seller[0].id
            return redirect("Seller:seller_home")
        else:
            message = 'invalid user or password'

    return render(request, 'customer/seller_login.html',{'status':message})


def customer_signup(request):
    message = ''
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']
        password = request.POST['password']

        # variable = request.POST['name attribute from html page']

        customer_exist = Customer.objects.filter(email = email).exists()
        # (value in models: variable)

        if not customer_exist:
            customer = Customer (first_name = first_name, last_name = last_name, gender = gender, email = email,city = city, country = country, password =password )
            customer.save()
            message = 'Registration successful'

        else:
             message = 'Email already Exists'


    return render(request, 'customer/customer_signup.html',{'status':message})


def customer_login(request):

    message = ''
    if request.method == 'POST':
        c_username = request.POST['email']
        c_password = request.POST['password']

        new_customer = Customer.objects.filter(email = c_username, password = c_password)
        # filter(name  from table = variable)

        if new_customer.exists():
            return redirect('customer:customer_home')
        else:
            message = 'incorrect username or password'

    return render(request, 'customer/customer_login.html',{'status':message})


def forgot_password_customer(request):
    return render(request, 'customer/forgot_password_customer.html')


def forgot_password_seller(request):
    return render(request, 'customer/forgot_password_seller.html')
from django.shortcuts import redirect,render
from random import randint
from django.conf import settings
from eKart_admin.models import Category, EkartAdmin
from seller.models import Seller
from django.core.mail import send_mail
from seller.models import Seller
# Create your views here.
def admin_home(request):
    return render(request,'ekart_admin/admin_home.html')

def admin_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = EkartAdmin.objects.get(user_name = username, passsword = password)
            return redirect('ekart_admin:admin_home')
        except Exception as e:
            print(e)
            message = 'Invalid Username Or Password'


    return render(request,'ekart_admin/admin_login.html', {'message': message})

def view_category(request):
    category_list = Category.objects.all()
    return render(request,'ekart_admin/view_category.html',{'category':category_list})

def add_category(request):
    message =''
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category_description = request.POST['description']
        category_picture = request.FILES['category_picture']

        category_exist = Category.objects.filter(category = category_name).exists()

        if not category_exist :
            category = Category(
                category = category_name,
                description = category_description,
                cover_picture = category_picture
            )
            category.save()

            message = 'Catergory added'
        else:
            message = 'category already existing'

    return render(request,'ekart_admin/add_category.html',{'status':message})

def pending_sellers(request):
    pending_list = Seller.objects.filter(status = 'pending')
    return render(request,'ekart_admin/pending_sellers.html',{'seller_list':pending_list})

def approve_seller(request,id):
    seller = Seller.objects.get(id = id)
    seller_id = randint(11111,99999)
    temporary_password = 'sel-' + str(seller_id)
    subject = 'login credentials'
    message = 'Hi your Ekart account has been approved,your username is '+str(seller_id) + 'and temporary password is '+str(temporary_password)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email]

    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list
    )

    Seller.objects.filter(id = id).update(login_id = seller_id, password = temporary_password, status = 'approved')

    return redirect('ekart_admin:pending_sellers')

def reject_sellers(request,id):
    seller = Seller.objects.get(id = id)
    subject = 'Account rejection'
    message = 'Hi your Ekart account has been rejected'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email]

    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list
    )

    Seller.objects.filter(id = id).update( status = 'rejected')
    

    return redirect('ekart_admin:pending_sellers')


def approved_sellers(request):
    approved_list = Seller.objects.filter(status = 'approved')
    return render(request,'ekart_admin/approved_sellers.html',{'approved_sellers':approved_list})

def rejected_sellers(request):
    rejected_list = Seller.objects.filter(status = 'rejected')
    return render(request,'ekart_admin/rejected_sellers.html',{'rejected_sellers':rejected_list})

def customers(request):
    return render(request,'ekart_admin/customers.html')
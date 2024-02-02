
import datetime
from random import randint
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import razorpay
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from customer.models import Answers, Cart, Customer, DeliveryAddress, Order, OrderItem, ProductQuestion, ProductReview, ReviewImage
from customer.rating import get_rating, get_star_rating
from eKart import settings
from seller.models import Product, Seller
from eKart_admin.models import Category
from django.db.models import Q,F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# from .models import Customer
# Create your views here.



def customer_home(request):
    # fetch the list of all categories
    category_list = Category.objects.all()
    
    # Fetch all products for the home page
    all_products = Product.objects.all()

    # Assuming you want to display a limited number of products on the home page
    item_per_page = 6

    paginator = Paginator(all_products, item_per_page)

    page = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'category_list': category_list,
        'product_count': paginator.count,
        'products': current_page,
        'current_page': current_page,
    }
    return render(request, 'customer/customer_home.html', context)
   


def store(request):
    # fetch the list of all categories
    category_list = Category.objects.all()
    print(category_list)
    
    query = request.GET.get('query')
    
    if query == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category = query)
        
    item_per_page = 6

    paginator=Paginator(products,item_per_page)

    page=request.GET.get('page',1)
    print("page=",page)
    try:
        current_page=paginator.page(page)
    except PageNotAnInteger:
        current_page=paginator.page(1)
    except EmptyPage:
        current_page=paginator.page(paginator.num_pages)
        


    if "search_text" in request.GET:
        search_text = request.GET.get('search_text')
        products = Product.objects.filter(Q(category__category__icontains = search_text) | Q(product_name__icontains = search_text))
        
    count = products.count()
    
    context = {
        'category_list' : category_list, 
        'product_count' : count,
        'products' : products,
        'product_count':paginator.count,
        'current_page':current_page,
    }
    return render(request, 'customer/store.html',context)


def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    already_reviewed = False
    try:
        customer = Customer.objects.get(id = request.session['customer'])
        already_reviewed = ProductReview.objects.filter(customer = customer, product = product_id).exists()
    
    except:
        None
    product = None

    questions = ProductQuestion.objects.filter(product = product_id)
    product = get_object_or_404(Product, id = product_id)

    reviews =  ProductReview.objects.filter(product = product_id)
    product_rating =reviews.values('rating').annotate(count = Count('rating'))
   
    
     
    rating_list = get_rating(product_id)

    review_count = ProductReview.objects.filter(product = product_id).count()
    
    
    star_rating = get_star_rating(rating_list)
    if request.method == 'POST':
        if 'customer' in request.session:
            cart = Cart(customer = customer, product = product, price = product.price)
            cart.save()
            return redirect('customer:cart',current_view = 'list')
        
        else:
            target_url = reverse('customer:customer_login')
             
            redirect_url =  target_url + '?pid=' + str(product_id)
            return redirect(redirect_url)
             
   
    
    try:

        cart_item = get_object_or_404(Cart, customer = customer,product = product_id)
        item_exist = True
        


    except Exception as e:
         
        item_exist = False
         


    context = {
        'product': product,
        'item_exist': item_exist,
        'review_count': review_count,
        'already_reviewed': already_reviewed,
        'product_rating': product_rating,
        'rating_list': rating_list,
        'star_rating': star_rating,
        'questions': questions,
        'reviews': reviews
         
        
    }    
   
    return render(request, 'customer/product_detail.html', context )

def cart(request, current_view):

    if 'customer' in request.session:
        print('*********')
        cart_items = Cart.objects.filter(customer = request.session['customer'])
        grand_total = 0
        customer = request.session['customer']
        disable_checkout = ''
        cart = Cart.objects.filter(customer = request.session['customer']).annotate(grand_total = F('quantity') * F('product__price') )
        
        for item in cart:
            grand_total += item.grand_total
        

        if not cart_items:
            disable_checkout = 'disabled'
        for item in cart_items:
        
            
            if item.product.stock == 0:
                disable_checkout = 'disabled'
                print(item.product.product_name,'not available')

        
        context = {
            'cart_items': cart_items, 
            'disable_checkout': disable_checkout, 
            'grand_total': grand_total,
            'total_items': cart_items.count(),
            
            }

        if request.method == 'POST':
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            phone = request.POST['phone']
            email = request.POST['email']
            state = request.POST['state']
            landmark = request.POST['landmark']
            house = request.POST['house']
            zipcode = request.POST['pincode']
            delivery_address = DeliveryAddress(first_name = first_name, last_name = last_name, email = email,
                                            customer_id = customer,state = state, landmark = landmark, phone = phone, house_name = house, pin_code = zipcode)
            
            delivery_address.save()
            
        if current_view == 'review':
            try:
                address_history = DeliveryAddress.objects.filter(customer = customer)

            except Exception as e:
                print(e)
                address_history = None
            if address_history:
                print(address_history)
                context['address_history'] = address_history
            return render(request, 'customer/cart_review.html', context)
        

        return render(request, 'customer/cart.html', context)
   
    return render(request, 'customer/cart.html')
    

def update_cart(request):
     
    product_id = request.POST['id']
    qty = request.POST['qty']
    print(qty)
    grand_total = 0
    cart = Cart.objects.get(product = product_id)
    cart.quantity = qty
    cart.save()

    cart = Cart.objects.filter(customer = request.session['customer']).annotate(grand_total = F('quantity') * F('product__price') )
    
    for item in cart:
        grand_total += item.grand_total
    
    # item_price = cart.product.price
    return JsonResponse({'status': 'Quantity updated', 'grand_total': grand_total})

def remove_cart_item(request, cart_id):

    try:
        selected_cart_item = Cart.objects.get(id = cart_id)
        selected_cart_item.delete()
    except:
        pass
    return redirect('customer:cart','list')


def review_cart(request):
    cart_items = Cart.objects.filter(customer = request.session['customer'])
    return render(request, 'customer/cart_review.html',{'cart_items': cart_items,})


def place_order(request):
    return render(request, 'customer/place_order.html')


def order_product(request):
    cart = Cart.objects.filter(customer = request.session['customer']).annotate(grand_total = F('quantity') * F('product__price') )

    customer = request.session['customer']
    grand_total = 0
    for item in cart:
       grand_total += item.grand_total
    
    order_amount = grand_total
    order_currency = 'INR'
    order_receipt ='order_rcptid_11'
    notes = {'shipping address':'bommanahalli,bangalore'}

     

    order_no = 'OD-Ekart-' + str(randint(1111111111,9999999999))
     
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY ,settings.RAZORPAY_API_SECRET))
    payment = client.order.create({
            'amount': order_amount * 100,
            'currency':order_currency,
            'receipt':order_receipt,
            'notes':notes,
             
        })
    
    order = Order(customer_id = customer, order_id = payment['id'], total_amount = grand_total, order_no = order_no )
    order.save()
    print(payment)
    return JsonResponse({'payment': payment})

def order_product(request):
    cart = Cart.objects.filter(customer = request.session['customer']).annotate(grand_total = F('quantity') * F('product__price') )

    customer = request.session['customer']
    grand_total = 0
    for item in cart:
       grand_total += item.grand_total
    
    order_amount = grand_total
    order_currency = 'INR'
    order_receipt ='order_rcptid_11'
    notes = {'shipping address':'bommanahalli,bangalore'}

     

    order_no = 'OD-Ekart-' + str(randint(1111111111,9999999999))
     
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY ,settings.RAZORPAY_API_SECRET))
    payment = client.order.create({
            'amount': order_amount * 100,
            'currency':order_currency,
            'receipt':order_receipt,
            'notes':notes,
             
        })
    
    order = Order(customer_id = customer, order_id = payment['id'], total_amount = grand_total, order_no = order_no )
    order.save()
    print(payment)
    return JsonResponse({'payment': payment})

@csrf_exempt
def update_payment(request):
    
    if request.method == 'GET':
        return redirect('customer:customer_home')

    order_id = request.POST['razorpay_order_id']
    payment_id = request.POST['razorpay_payment_id']
    signature = request.POST['razorpay_signature']
    client = razorpay.Client(auth = (settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }
    signature_valid = client.utility.verify_payment_signature(params_dict)
    if signature_valid:
    
        order_details = Order.objects.get(order_id = order_id)
        order_details.payment_status = True
        order_details.payment_id = payment_id
        order_details.signature_id = signature
        order_details.order_status = 'order placed on ' + str(datetime.date.today())
        customer=Customer.objects.get(id=order_details.customer_id)
        cart = Cart.objects.filter(customer = customer)

        for item in cart:
            order_item = OrderItem(order_id = order_details.id, customer_id =  customer.id, product_id = item.product.id, quantity = item.quantity, price = item.product.price )
            order_item.save()
            selected_qty = item.quantity
            selected_product = Product.objects.get(id = item.product.id)
            selected_product.stock -= selected_qty
            selected_product.save()
            

   
        order_details.save()
        cart.delete()

        customer_name = customer.first_name
        order_number =  order_details.order_no
        current_year = datetime.now().year
        
        subject = "Order Confirmation"
        from_email = settings.EMAIL_HOST_USER

        to_email = ['suvarna@cybersquare.org']
    
    return render(request, 'customer/order_complete.html',  )

def product_review(request,id):
    purchased = OrderItem.objects.filter(product = id, customer = request.session['customer'] ).exists()
    if request.method == 'POST':
        customer = request.session['customer']
        title = request.POST['title']
        review = request.POST['customer_review']
        star_count = request.POST['star_count']

        customer_review = ProductReview(product_id = id, customer_id = customer,
                                         title = title, review = review, rating = star_count)
        customer_review.save()
        if request.FILES:
            for image in request.FILES.getlist('images'):
                 
                review_image = ReviewImage(review_id = customer_review.id, image = image)
                review_image.save()
        
        rating_list = get_rating(id)
        star_rating = get_star_rating(rating_list) 
        Product.objects.filter(id = id).update(rating = star_rating)
    return render(request, 'customer/product_review.html', {'purchased': purchased})


def add_product_qstn(request, product_id):

    if request.method == 'POST':
        question = request.POST['question']
        
        product_question = ProductQuestion(customer_id = request.session['customer'], 
                                           product_id = product_id, question = question)
        
        product_question.save()

        return redirect('customer:product_detail', product_id)
    return render(request, 'customer/post_questions.html',)


def display_qstn_details(request):
    qnstn_id = request.GET['qstnId']
    answer_set = Answers.objects.filter(question = qnstn_id)
     
    serialized_data = [{'id': answer.id, 'answer': answer.answer, 'customer': answer.customer.first_name} for answer in  answer_set]

    print(serialized_data)

    return JsonResponse({'data': serialized_data,})

def review_cart(request):
    cart_items = Cart.objects.filter(customer = request.session['customer'])
    return render(request, 'customer/cart_review.html',{'cart_items': cart_items,})

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
    message = ""
    if request.method == "POST":
        username = request.POST["sellerId"]
        password = request.POST["password"]
        
        seller = Seller.objects.filter(login_id = username, password = password)
        if seller.exists():
            request.session['seller'] = seller[0].id
            return redirect('Seller:seller_home')
        else:
            message = 'invalid username or password'
        
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

        new_customer = Customer.objects.filter(email = c_username, password = c_password).first()
        # filter(name  from table = variable)

        if new_customer:
            request.session['customer']=new_customer.id
            return redirect('customer:customer_home')
        else:
            message = 'incorrect username or password'

    return render(request, 'customer/customer_login.html',{'status':message})


def forgot_password_customer(request):
    return render(request, 'customer/forgot_password_customer.html')


def forgot_password_seller(request):
    return render(request, 'customer/forgot_password_seller.html')
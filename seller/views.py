from django.shortcuts import get_object_or_404, redirect, render
from eKart_admin.models import Category
from seller.models import Product, Seller

# Create your views here.
def seller_home(request):
    return render(request, 'seller/seller_home.html')

def add_product(request):
    #fetch all category from the database
    category_list = Category.objects.all()
    # Initialize an empty message variable
    msg = ''

    # check if the form is submitted using post method

    if request.method =="POST":

    #retrive data from the form sunbmission
        product_no =  request.POST['product_code']
        product_name = request.POST['product_name']
        category = request.POST['category']
        description = request.POST['description']
        stock = request.POST['stock']
        price = request.POST['price']
        image = request.FILES['image']
        seller = request.session['seller']



        #use get_or_create to either existing or create a new product

        product,created = Product.objects.get_or_create (
            product_no = product_no,
            seller = Seller.objects.get(id = seller),
            defaults = {
                'product_no' : product_no,
                'product_name' : product_name.lower(),
                'seller' : Seller.objects.get(id = seller),
                'category' : Category.objects.get(id = category),
                'description' : description.lower(), 
                               
                'stock' : stock,
                'price' : price,
                'image' : image,
            }
        )
        
        if created:
            msg = 'product added'
        else:
            msg= 'product no already exist'

#prepare the context to be psssed to the template
    context = {
    'category' : category_list,
    'message' : msg
    }

        #render the 'add_product.html' template with the provides context
    return render(request, 'seller/add_product.html',context)

def add_category(request):
    return render(request, 'seller/add_category.html')

def view_category(request):
    return render(request, 'seller/view_category.html')

def view_products(request):
    product_list = Product.objects.filter(seller_id = request.session['seller'])
    return render(request, 'seller/view_product.html',{'products': product_list})

def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller_id=request.session['seller'])

    # Perform any additional validation or logic before deleting
    # For example, you might want to check if the product is in the user's inventory.

    product.delete()
    return redirect('seller:view_product')

def profile(request):
    return render(request,'seller/profile.html')

def view_orders(request):
    return render(request,'seller/view_orders.html')

def update_stock(request):
    return render(request,'seller/update_stock.html')

def order_history(request):
    return render(request,'seller/order_history.html')
from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [   
   path('',views.customer_home, name='customer_home'),
   path('store',views.store,name='store'),
   path('product/detail/<int:item_id>',views.product_detail,name='product_detail'),
   path('cart',views.cart,name='cart'),
   path('cart/item/update',views.update_cart,name='update_cart'),
   path('cart/item/remove/<int:cart_id>',views.remove_cart_item,name='remove_cart_item'),
   path('placeOrder',views.place_order,name='place_order'),
   path('order/successc',views.order_complete,name='order_complete'),
   path('order/complete/>',views.update_payment,name='update_payment'),
   path('customer/products/order', views.order_product, name = 'order_product'),
   path('dashboard',views.dashboard,name='dasboard'),
   path('seller/register',views.seller_register,name='seller_register'),
   path('seller/login',views.seller_login,name='seller_login'),
   path('customer/signup',views.customer_signup,name='customer_signup'),
   path('customer/login',views.customer_login,name='customer_login'),
   path('forgotPassword/customer',views.forgot_password_customer,name='forgot_password_customer'),
   path('forgotPassword/seller',views.forgot_password_seller,name='forgot_password_seller'),
   

]

import imp
from wsgiref import validate
from django.http import HttpResponse
from django.shortcuts import redirect, render

from store.models.orders import Order
from .models.product import Product
from .models.product import Category
from .models.customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from.middlewares.auth import auth_middleware
from.middlewares.auth1 import auth_middleware1
from django.utils.decorators import method_decorator


class Index(View):
    def get(self,request):
        pro=None
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        cat=Category.get_all_categories()
        categoryId=request.GET.get('category')
        if categoryId:
            pro=Product.get_all_products_by_categoryid(categoryId)
        else:
            pro=Product.get_all_products()
        data={}
        data['products']=pro
        data['categories']=cat
        data['session_create']=request.session.get('email')
        return render(request,'index.html',data)

    def post(self,request):
        product=request.POST.get('product')
        cart=request.session.get('cart')
        minus_val=request.POST.get('minus')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if minus_val:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart
        print(request.session['cart'])
        return redirect('homepage') 

# Create your views here.


def validation(cust): 
    error_message=None
    if (not cust.first_name):
        error_message='First name rquired !!'
    elif len(cust.phone) < 10:
        error_message=' Phone number must be 10 characters long !!'
    elif len(cust.password) < 8:
        error_message=' Password must be 8 characters long !!'
    elif cust.isExists():
        error_message='Email ID already exists'
    return error_message


def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
            
        value={
                'first_name':first_name,
                'last_name':last_name,
                'phone':phone,
                'email':email
        }

        cust=Customer(
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        password=password
        )
        error_message=validation(cust)
        #saving
        if not error_message:
            print(first_name,last_name,phone,email,password)
            cust.password=make_password(cust.password)
            cust.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request,'signup.html',data)



class login(View):
    def get(self,request):
         return render(request,'login.html')
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        cust=Customer.get_customer_by_email(email)
        error_message=None
        if cust:
            flag=check_password(password,cust.password)
            if flag:
                request.session['customer_id']=cust.id
                request.session['email']=cust.email
                return redirect('homepage')
            else:
                error_message='Email or password invalid !!'
                return render(request,'login.html',{'error':error_message})
        else:
            error_message='Email or password invalid !!'
            return render(request,'login.html',{'error':error_message})






def logout(request):
    request.session.clear()
    return redirect('loginpage')




class cart_page(View):
    @method_decorator(auth_middleware)#for checking whether the customer is login or not
    @method_decorator(auth_middleware1)#for checking whether the product is in cart or not
    def get(self,request):
        ids=(list(request.session.get('cart').keys()))
        Products=Product.get_products_by_id(ids)
        print(Products)
        return render(request,'cart.html',{'Products':Products})


class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer_id')
        cart=request.session.get('cart')
        pro=Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer,cart,pro)
        for i in pro:
            order=Order( product=i,
            customer=Customer(id=customer),
            quantity=cart.get(str(i.id)),
            price=i.price,
            address=address,
            phone=phone
            )
            order.save()
        request.session['cart']={}
        return redirect('cartpage')


class orders_view(View):
    def get(self,request):
        customer=request.session.get('customer_id')
        orders=Order.get_orders_by_customer_id(customer)
        print(orders)
        return render(request,'orders.html',{'orders':orders})






















"""

def index(request):
    pro=None
    cat=Category.get_all_categories()
    categoryId=request.GET.get('category')
    if categoryId:
        pro=Product.get_all_products_by_categoryid(categoryId)
    else:
        pro=Product.get_all_products()
    data={}
    data['products']=pro
    data['categories']=cat
    data['session_create']=request.session.get('email')
    return render(request,'index.html',data)




def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        cust=Customer.get_customer_by_email(email)
        error_message=None
        if cust:
            flag=check_password(password,cust.password)
            if flag:
                return redirect('homepage')
            else:
                error_message='Email or password invalid !!'
                return render(request,'login.html',{'error':error_message})
        else:
            error_message='Email or password invalid !!'
            return render(request,'login.html',{'error':error_message})

    

    """

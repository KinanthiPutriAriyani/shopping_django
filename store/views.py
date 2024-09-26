from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail
from django.db.models import Q

#============================Home Page===============================
def home(request):
    products = None
    totalitem = 0
    if request.session.has_key('username'):
        username = request.session['username']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(username=username)
        totalitem = len(Cart.objects.filter(username=username))
        
        # Ambil produk berdasarkan kategori
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_category_id(categoryID)
        else:
            products = Product.get_all_products()

        data = {
            'username': username,
            'product': products,
            'category': category,
            'totalitem': totalitem
        }
        return render(request, 'home.html', data)
    else:
        return redirect('login')


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        email = postData.get('email')
        address = postData.get('address')
        contact_no = postData.get('contact_no')
        paypal_id = postData.get('paypal_id')
        date_of_birth = postData.get('dob')
        gender = postData.get('gender')
        city = postData.get('city')

        error_message = None

        # Validasi input
        if not username:
            error_message = "Username is Required"
        elif not password:
            error_message = "Password is Required"
        elif not email:
            error_message = "Email is Required"
        elif not address:
            error_message = "Address is Required"
        elif not contact_no:
            error_message = "Contact number is Required"
        elif not paypal_id:
            error_message = "PayPal ID is Required"
        elif not date_of_birth:
            error_message = "Date of Birth is Required"
        elif not gender:
            error_message = "Gender is Required"
        elif not city:
            error_message = "City is Required"
        elif len(contact_no) < 10:
            error_message = "Contact Number must be more than 10 characters"
        elif Customer.objects.filter(username=username).exists():
            error_message = "Username already exists"

        # Simpan customer jika tidak ada error
        if not error_message:
            customer = Customer(
                username=username,
                password=password,
                email=email,
                address=address,
                contact_no=contact_no,
                paypal_id=paypal_id,
                date_of_birth=date_of_birth,
                gender=gender,
                city=city
            )
            customer.register()  # Pastikan Anda memiliki metode register di model Customer
            messages.success(request, 'Congratulations, Registration is Successful!')
            return redirect('login')  # Redirect ke halaman login setelah berhasil mendaftar
        else:
            data = {
                'error': error_message,
                'value': {
                    'username': username,
                    'email': email,
                    'address': address,
                    'contact_no': contact_no,
                    'paypal_id': paypal_id,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'city': city
                }
            }
            return render(request, 'signup.html', data)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error_message = None
        value = {'username': username, 'password': password}
        
        customer = Customer.objects.filter(username=username).first()

        if customer:
            if password == customer.password:
                request.session['username'] = username
                return redirect('homepage')
            else:
                error_message = "Invalid password"
        else:
            error_message = "Invalid username"

        data = {'error': error_message, 'value': value}
        return render(request, 'login.html', data)


def productdetail(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.session.has_key('username'):
        username = request.session["username"]
        totalitem = len(Cart.objects.filter(username=username))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(username=username)).exists()

        data = {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'username': username,
            'totalitem': totalitem
        }
        return render(request, 'productdetail.html', data)


def logout(request):
    if request.session.has_key('username'):
        del request.session["username"]
    return redirect('login')


def add_to_cart(request):
    username = request.session['username']
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    cart_item = Cart.objects.filter(product=product, username=username).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            username=username,
            product=product,
            image=product.image,
            price=product.price,
            quantity=1
        )

    return redirect(f"/product-detail/{product_id}")


def show_cart(request):
    if request.session.has_key('username'):
        username = request.session["username"]
        cart_items = Cart.objects.filter(username=username)
        totalitem = len(cart_items)

        data = {
            'username': username,
            'totalitem': totalitem,
            'cart_items': cart_items
        }

        if cart_items.exists():
            return render(request, 'show_cart.html', data)
        else:
            return render(request, 'empty_cart.html', data)
        

def update_cart_quantity(request, cart_item_id):
    if request.method == 'POST':
        change = int(request.POST.get('change', 0))
        cart_item = Cart.objects.get(id=cart_item_id)

        # Update quantity
        cart_item.quantity += change

        # Ensure quantity does not go below 1
        if cart_item.quantity < 1:
            cart_item.quantity = 1

        cart_item.save()
        return redirect('show_cart')


def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('show_cart')


def checkout(request):
    totalitem=0
    if request.session.has_key('username'):
        username = request.session['username']
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        cart_product = Cart.objects.filter(username=username)
        for c in cart_product:
            qty = c.quantity
            price = c.price
            product_name = c.product
            OrderDetail(user=username, product_name=product_name, qty=qty, price=price).save()
            cart_product.delete()
            totalitem = len(Cart.objects.filter(username=username))
            customer = Customer.objects.filter(username=username)
            for c in customer:
                username=c.username
            data={
                'username':username,
                'totalitem':totalitem,
                'address':address,
                'mobile':mobile
            }
            return render(request, 'empty_cart.html',data)
    else:
        return redirect('login')
    
def order(request):
    totalitem=0
    if request.session.has_key('username'):
        username = request.session['username']
        totalitem = len(Cart.objects.filter(username=username))
        order = OrderDetail.objects.filter(user=username)
        customer = Customer.objects.filter(username=username)
        for c in customer:
            username=c.username
        data ={
        'order':order,
        'username':username,            
        'totalitem':totalitem
         }
        if order:
            return render(request, 'order.html',data)
        else:                 
            return render(request, 'emptyorder.html',data)        
    else:
        return redirect('login')
    
def search(request):
    totalitem=0
    if request.session.has_key('username'):
        username = request.session['username']
        query = request.GET.get('query')
        # print(query)
        search = Product.objects.filter(name__contains=query)
        category = Category.get_all_categories()
        totalitem = len(Cart.objects.filter(username=username))
        customer = Customer.objects.filter(username=username)
        for c in customer:
            username = c.username
        data ={
            'username':username,
            'totalitem':totalitem,
            'search':search,
            'category':category,
            'query':query
        }
        return render(request, 'search.html', data) 
    else:
        return redirect('login')  


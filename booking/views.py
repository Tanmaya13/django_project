from turtle import st
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q

# Create your views here.
def index(request):
    services = Services.objects.all()
    products = []
    user = get_active()
    print(user)
    for service in services:
        print(service)
        prods = Product.objects.filter(sid=service)
        for prod in prods:
            print(prod)
            imgs = ProductImage.objects.filter(product=prod)
            print(imgs)
            products.append([prod, imgs])
    
    context = {
        'services': services,
        'products': products,
        'msg': '',
        'user': user
        }
    return render(request, 'index.html', context=context)

def signIn(request):
    return render(request, 'signIn.html')

def loginUser(request):
    if request.method=='GET':
        phone = request.GET.get('phone')
        if phone[0] == '0':
            phone = phone[1:]
        user = get_active()
        if user is not None:
            user.logged_in = False
            user.save()
        user = User.objects.get(phone=phone)
        print(user)
        user.logged_in = True
        print(user.logged_in)
        user.save()
        return HttpResponseRedirect('/')

def services_show(request, sid):
    services = Services.objects.all()
    s = Services.objects.get(sid=sid)
    user = get_active()
    if s.service_name == 'All':
        return HttpResponseRedirect('/allServices/')
    else:
        products = Product.objects.filter(sid=s)
        prod_list = []
        for product in products:
            img = ProductImage.objects.filter(product=product)[:1]
            prod_list.append([product, img])
    
        context = {
            'services': services,
            's': s,
            'products': prod_list,
            'msg': '',
            'user': user
            }
        return render(request, 'service.html', context=context)

def allServices(request):
    services = Services.objects.all()
    products = Product.objects.all()
    user = get_active()

    context = {
        'services': services,
        'products': products,
        'msg': '',
        'user': user
        }
    return render(request, 'allServices.html', context=context)

def take(request, id):
    if request.method=='GET':
        sid = request.GET.get('sid')
        return HttpResponseRedirect('/show-service/{}/'.format(sid))

def cart(request):
    if request.method=='GET':
        adults = request.session['adults'] = int(request.GET.get('adults'))
        children = request.session['children'] = int(request.GET.get('children'))
        arrival =  request.GET.get('arrival')
        time =  request.GET.get('time')
        pid =  request.session['pid'] =  request.GET.get('pid')
        user = get_active()

        prod = Product.objects.get(pid=pid)

        year, month, day = map(str, arrival.split('-'))
        arrival_date = request.session['arrival_date'] = year + month + day
        arrival_date = datetime.datetime.strptime(arrival_date, "%Y%m%d").date()       

        hour, minute = map(str, time.split(':'))
        request.session['arrival_time'] = hour + ':' + minute + ':00.00'
        
        
        if prod.available_from <= arrival_date <= prod.available_till:
            img = ProductImage.objects.filter(product=prod)[0]
            adult_total = adults*prod.price_per_person
            child_total = children*prod.child_price
            total = adult_total + child_total
            
            orig = adults*100 + children*65
            discount = orig - total

            context = {
                'prod': prod,
                'total': total,
                'discount': discount, 
                'adults': adults,
                'children': children,
                'arrival': arrival, 
                'time': time, 
                'orig': orig, 
                'img': img,
                'user': user
                }
            return render(request, 'cart.html', context=context)
        else:
            msg = 'Please Select from Available Dates'
            return HttpResponseRedirect('/product/{}/{}/'.format(pid, msg))

def login_or_create(phone, name, email):
    try:
        user = User.objects.get(phone=phone)
        us = get_active()
        us.logged_in = False
        us.save()
        user.logged_in = True
        user.save()
    except User.DoesNotExist:
        user = User(name=name, email=email, phone=phone)
        user.save()
    return user

def get_active():
    try:
        user = User.objects.get(logged_in=True)
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        users = User.objects.filter(logged_in=True)
        for u in users:
            u.logged_in = False
            u.save()
        return None

def checkout(request):
    if request.method=='GET':
        name = request.GET.get('fname') + ' ' + request.GET.get('lname')
        phone = request.GET.get('phone')
        email = request.GET.get('email')

        user = get_active()
        if user is not None:
            if user.phone == phone:
                pass
            else:
                login_or_create(phone, name, email)
        else:
            login_or_create(phone, name, email)

        adults = int(request.session['adults'])
        children = int(request.session['children'])
        pid =  int(request.session['pid'])

        product = Product.objects.get(pid=pid)
        adult_total = adults*product.price_per_person
        child_total = children*product.child_price
        total = request.session['total'] = adult_total + child_total
        guests = adults + children

        context = {
            'prod': product, 
            'adults': adults, 
            'children': children, 
            'child_total': child_total, 
            'adult_total': adult_total, 
            'total': total, 
            'guests': guests,
            'user': user
            }
        return render(request, 'checkout.html', context=context)

def makeBooking(request):
    if request.method == 'GET':
        arrival_date = request.session['arrival_date']
        arrival_time = request.session['arrival_time']
        car = request.GET.get('car')
        airport = request.GET.get('airport')
        user = get_active()
        pid = request.session['pid']
        product = Product.objects.get(pid=int(pid))

        if car == 'yes':
            car_ser = True
        else:
            car_ser = False
        if airport == 'yes':
            airport_ser = True
        else:
            airport_ser = False

        arrival_date = datetime.datetime.strptime(arrival_date, "%Y%m%d").date()
        arrival_time = datetime.datetime.strptime(arrival_time, "%H:%M:%S.%f").time()

        booking = Bookings(arrival_date=arrival_date, arrival_time=arrival_time, user=user, product=product,
        car_service=car_ser, pickup_from_airport=airport_ser, adults=int(request.session['adults']),
        children=int(request.session['children']), total=int(request.session['total']))
        booking.save()

        context = {
            'user': user
        }
        return render(request, 'confirmed.html', context=context)

def show_booking(request, bid):
    booking = Bookings.objects.get(bid=bid)
    product = booking.product

    main = ShowImages.objects.filter(product=product, image_position='Main')
    side_1 = ShowImages.objects.filter(product=product, image_position='Side')[:2]
    side_2 = ShowImages.objects.filter(product=product, image_position='Side')[2:]
    user = get_active()

    context = {
        'main': main, 
        'side_1': side_1, 
        'side_2': side_2, 
        'b': booking,
        'user': user
        }
    return render(request, 'booking_details.html', context=context)

def bookings(request):
    mybookings = []
    bookings = Bookings.objects.filter(user=get_active())
    for booking in bookings:
        img = ProductImage.objects.filter(product=booking.product)[:1]
        mybookings.append([booking, img])

    context = {
        'user': get_active(),
        'bookings': mybookings
    }
    return render(request, 'bookings.html', context=context)

def show_product_msg(request, pid, msg):
    product = Product.objects.get(pid=pid)
    service = Services.objects.get(service_name='Packages')
    prods = Product.objects.filter(~Q(pid=pid), sid=service).order_by('-pid')[:3]
    user = get_active()
    recommend = []
    for prod in prods:
        imgs = ProductImage.objects.filter(product=prod)
        recommend.append([prod, imgs])
    main = ShowImages.objects.filter(product=product, image_position='Main')
    side_1 = ShowImages.objects.filter(product=product, image_position='Side')[:2]
    side_2 = ShowImages.objects.filter(product=product, image_position='Side')[2:]

    context = {
        'product': product, 
        'recommend': recommend, 
        'main': main, 
        'side_1': side_1, 
        'side_2': side_2, 
        'msg': msg,
        'user': user
        }
    return render(request, 'single-product.html', context=context)

def show_product(request, pid):
    product = Product.objects.get(pid=pid)
    service = Services.objects.get(service_name='Packages')
    prods = Product.objects.filter(~Q(pid=pid), sid=service).order_by('-pid')[:3]
    user = get_active()
    recommend = []
    for prod in prods:
        imgs = ProductImage.objects.filter(product=prod)
        recommend.append([prod, imgs])
    main = ShowImages.objects.filter(product=product, image_position='Main')
    side_1 = ShowImages.objects.filter(product=product, image_position='Side')[:2]
    side_2 = ShowImages.objects.filter(product=product, image_position='Side')[2:]

    context = {
        'product': product, 
        'recommend': recommend, 
        'main': main, 
        'side_1': side_1, 
        'side_2': side_2, 
        'msg': '',
        'user': user
        }
    return render(request, 'single-product.html', context=context)

def logout(request):
    user = get_active()
    user.logged_in = False
    user.save()
    return redirect('index')
from app.models import customers,Orders,Payment,PasswordResetRequest
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, HttpResponse
from datetime import date
import time
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "index.html")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        error_message=''
        error_message1=''
        if not username and not password:
            error_message2="Missing credentials"
            return render(request,"login.html",{'error2':error_message2})

        elif not username or not password:
            if not username:
                error_message="username should not be empty"
            elif not password:
                error_message1="password should not be empty"
            return render(request,"login.html",{'error':error_message,'error1':error_message1})

        try:
            user = customers.objects.get(username=username)
        except customers.DoesNotExist:
            error_message='username does not exist'
            return render(request,'login.html',{'error':error_message})

        if not check_password(password, user.password):
            error_message = 'Entered wrong password'
            return render(request, 'login.html', {'error1': error_message})

        request.session['user_id'] = user.id
        return redirect('home')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        error_message = ''
        error_message1 = ''
        error_message2 = ''
        if customers.objects.filter(username=username).exists():
            error_message="username already taken"
        elif not username:
            error_message="username field should not be empty"
        elif len(username)<=4:
            error_message="username should be more than 4 characters"
        if customers.objects.filter(email=email).exists():
            error_message2="Email already registered"
        if password!=confirm_password:
            error_message1="password and confirm password are not matching"
        if not error_message and not error_message1:
            hashed_password = make_password(password)
            customer = customers(
                username=username,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                password=hashed_password
            )
            customer.save()
            return redirect('login')
        else:
            return render(request, 'signup.html',{'error':error_message,'error1':error_message1,'error2':error_message2})

    return render(request, 'signup.html')


def home(request):
    user_id = request.session.get('user_id')
    user = customers.objects.get(id=user_id)
    username = user.username
    orders = Orders.objects.filter(username=username).order_by('-id')[:10]

    context = {
        'orders': orders
    }
    return render(request, 'home.html',context)


def signoff(request):
    request.session.clear()
    return redirect('index')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def search_food(request):
    if request.user.is_authenticated:
        return redirect('menu')

    return render(request, 'menu.html')



def order(request):
    user_id = request.session.get('user_id')
    try:
        user = customers.objects.get(id=user_id)
    except customers.DoesNotExist:
        return HttpResponse("User not found")
    order_id = str(int(time.time())) + '_' + str(user.id)
    username = user.username
    order_date = date.today()
    order_time = time.strftime("%H:%M:%S", time.localtime())
    context ={
        'username' : username,
        'order_id' : order_id,
        'order_date':order_date,
        'order_time':order_time
        }

    if request.method == 'POST':

        username = request.POST.get('username')
        order_id = request.POST.get('order_id')
        order_date = request.POST.get('order_date')
        order_time = request.POST.get('order_time')
        total_amount = request.POST.get('price')
        delivery_address=request.POST.get('address')
        orders = Orders(
            username=username,
            order_id=order_id,
            order_date=order_date,
            order_time=order_time,
            delivery_address=delivery_address,
            total_amount=total_amount)
        orders.save()
        return redirect('payment')

    return render(request, 'order_summary.html',context)


def payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        cardholder= request.POST.get('cardholder')
        expirydate = request.POST.get('expirydate')
        cvv = request.POST.get('cvv')
        hash_expirydate=make_password(expirydate)
        hash_cvv = make_password(cvv)
        payments = Payment(
            card_number=card_number,
            cardholder=cardholder,
            expirydate=hash_expirydate,
            cvv=hash_cvv)
        payments.save()
        return redirect('home')

    return render(request, 'payment.html')


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = customers.objects.get(username=username)
            email = user.email
            characters = string.digits
            otp = ''.join(random.choice(characters) for _ in range(6))
            user=customers.objects.get(email=email)
            user_id=user.id

            passwordResetRequest=PasswordResetRequest(
                email=email,
                otp=otp,
                user_id=user_id
            )
            passwordResetRequest.save()
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('password_reset_confirmation')
        except customers.DoesNotExist:
            error_message = "Username does not exist."
            return render(request,'password_reset.html',{'error':error_message})

    return render(request, 'password_reset.html')


def password_reset_confirmation(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if otp=='' and not (password == '' and confirm_password == ''):
            error_message="Please enter valid OTP"
            return render(request, 'password_reset_confirmation.html',{'error':error_message})
        elif password=='' and not (otp == '' and confirm_password == ''):
            error_message1="Please enter password"
            return render(request, 'password_reset_confirmation.html',{'error1':error_message1})
        elif confirm_password=='' and not (otp == '' and password == ''):
            error_message2="Please enter confirm password"
            return render(request, 'password_reset_confirmation.html',{'error2':error_message2})

        if password != confirm_password:
            error_message = "password and confirm password are not same"
            return render(request, 'password_reset_confirmation.html', {'error3': error_message})

        try:
            password_resets = PasswordResetRequest.objects.get(otp=otp)
            email=password_resets.email
            user = customers.objects.get(email=email)

            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()
            return redirect('login')

        except PasswordResetRequest.DoesNotExist:
            error_message="Please enter valid OTP"
            return render(request, 'password_reset_confirmation.html',{'error': error_message})

    return render(request, 'password_reset_confirmation.html')

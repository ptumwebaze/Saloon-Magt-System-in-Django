import json
import urllib
from django.db.models.expressions import F
from django.http.response import Http404
# from django.config import settings
from django.shortcuts import render,redirect
from django.urls.resolvers import URLResolver
from django.utils import timezone
from django.contrib import messages
#from django.contrib import simpledialog
from django.forms.utils import ErrorList
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import uuid, base64, json
from datetime import date, datetime
import random
import sys
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django import template
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, employee_up, serviceup, orderup, orderdetailup, cartup, expenseup
from .models import user_reg, service, cart, order, orderdetail, logs, employee, expense

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            activity = username+" "+"successfully logged into the system"
            if user is not None:
                login(request, user)
                create = logs.objects.create(activity=activity, user=username)
                return redirect("/dashboard/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/index.html", {"form": form, "msg" : msg})

def register(request):
    msg     = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                form.save()
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('/register/')

            form.save()
            first_name = form.cleaned_data.get("firstname")
            last_name = form.cleaned_data.get("lastname")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            activity = "Successfull registered a new account for"+" "+username
            user = authenticate(first_name=first_name,last_name=last_name,username=username,email=email,password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            create = logs.objects.create(activity=activity, user=username)
            messages.success(request, 'Registration successfull!')
            return redirect('/')

        else:
            msg = 'Form is not valid'            
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success})


@login_required(login_url="/")
def commissionpage(request):
    employ = employee.objects.all()
    return render(request, "commission.html", {"employees":employ})

@login_required(login_url="/")
def salespage(request):
    sales = orderdetail.objects.all()
    return render(request, "sales.html", {"allsales":sales})

@login_required(login_url="/")
def commpay(request):
    if request.method == 'POST':
        employ = employee.objects.all()
        amounts = request.POST["paid"]
        id = request.POST["id"]
        paid = employee.objects.filter(id=id).update(paid=F('paid') + amounts)
        balance = employee.objects.filter(id=id).update(balance=F('balance') - amounts)
        return render(request, "commission.html", {"employees": employ})

@login_required(login_url="/")
def expenses(request):
    allexpenses = expense.objects.all()
    return render(request, "expenses.html", {"expenses":allexpenses})

def expense_submit(request):    
    if request.method == 'POST':
        name = request.POST["name"]
        amount = request.POST["amount"]
        description = request.POST["description"]
        username = request.user.username
        activity = "expense"+" "+name+" "+"registered successfully"
        
        serve = expense.objects.create(name=name, amount=amount, description=description, addedby=username)
        create = logs.objects.create(activity=activity, user=username)
        messages.success(request, 'Expense '+name+' successfully registered')
        return redirect('/expense/')
    else: 
        messages.info(request, 'Connection aborted, Please try again')
        return render(request, 'expenses.html')

def expense_edit(request, pk=None):
    expenses= get_object_or_404(expense, id=pk)
    form = expenseup(request.POST or None, instance=expenses)
    username = request.user.username
    activity = "expense"+" "+expenses.name+" "+"update successfully"
    if form.is_valid():            
            instance=form.save(commit=False)            
            instance.save()
            create = logs.objects.create(activity=activity, user=username)
            messages.success(request, 'Expense successfully updated')                
            return redirect('/expense/')
    context = {'form':form}
    return render(request, 'expenses.html', context)

def expense_delete(request, pk):
    expensedel= get_object_or_404(expense, id=pk)
    if request.method == 'POST':
        expensedel.delete()
        return redirect('/expense/')
    return render(request, 'expenses.html')


@login_required(login_url="/")
def debtors(request):
    debtor = order.objects.filter(balance__gt= 0)
    return render(request, "debtors.html", {"debtorsobj": debtor})

@login_required(login_url="/")
def servepage(request):
    serve = service.objects.all()
    return render(request, "service.html", {"service": serve})

@login_required(login_url="/")
def debt_pays(request):
    if request.method == 'POST':
        alldebtor = order.objects.filter(balance__gt= 0)
        amounts = request.POST["paid"]
        id = request.POST["id"]
        paid = order.objects.filter(id=id).update(paid=F('paid') + amounts)
        balance = order.objects.filter(id=id).update(balance=F('balance') - amounts)
        return render(request, "debtors.html", {"debtorsobj": alldebtor})

@login_required(login_url="/")
def dashboard(request):
    print(request.user.email)
    today = date.today()
    orderthis = order.objects.filter(added_on__day=today.day, added_on__month=today.month, added_on__year=today.year).count()
    usercount = User.objects.all().count()
    expenses = expense.objects.all().count()
    count_order = order.objects.all().count()
    count_employee = employee.objects.all().count()
    return render(request, "dashboard.html", {"employee":count_employee,"expense": expenses, "order": orderthis, "order": count_order,  "user": usercount, })


def incartpage(request):
    serve = service.objects.all()
    return render(request, "service.html", {"service": serve})
@login_required(login_url="/")
def homepage(request):
    serve = service.objects.all()
    return render(request, "home.html", {"service": serve})
@login_required(login_url="/")
def cartpage(request):
    cartadd = cart.objects.all()
    print(cartadd)
    return render(request, "cart.html", {"cart": cartadd})
    
def cart_del(request, pk):
    cartob= get_object_or_404(cart, id=pk)
    username = request.user.username
    activity = "cart"+" "+cartob.name+" "+cartob.item_name+" "+"deleted successfully"
    if request.method == 'POST':
        cartob.delete()
        create = logs.objects.create(activity=activity, user=username)
        return redirect('/cart/')
    return redirect('/service.html/')
 
@login_required(login_url="/")
def clientpage(request):
    clientadd = user_reg.objects.all()
    return render(request, "client.html", {"user_reg": clientadd})

@login_required(login_url="/")
def logspage(request):
    log = logs.objects.all()
    return render(request, "logs.html", {"logs": log})


@login_required(login_url="/")
def orderspage(request):
    serve = service.objects.all()
    carts = cart.objects.all()
    
    return render(request, "orders.html", {"cart": carts, "service":serve})

@login_required(login_url="/")
def ordermgt(request):
    serve = service.objects.all()
    employ = employee.objects.all()
    carts = cart.objects.all()
    cartam = 0
    for cartamount in carts:
        cartam = cartam+cartamount.service_price
    return render(request, "ordermgt.html", {"employees":employ, "cart": carts, "service":serve, "cartamount":cartam})


@login_required(login_url="/")
def userorder(request):
    order = order.objects.all()
    return render(request, "userorder.html", {"orders": order})


def employeespage(request):
    prof = employee.objects.all()
    return render(request, "employees.html", {"employees": prof})

def service_regist(request):    
    if request.method == 'POST':
        name = request.POST["name"]
        selling_price = request.POST["selling_price"]
        commission = request.POST["commission"]
        cost_price = request.POST["cost_price"]
        username = request.user.username
        activity = "service"+" "+name+" "+"registered successfully"
        
        serve = service.objects.create(name=name, selling_price=selling_price, commission=commission, cost_price=cost_price, addedby=username)
        create = logs.objects.create(activity=activity, user=username)
        messages.success(request, 'Service '+name+' successfully registered')
        return redirect('/service/')
    else: 
        messages.info(request, 'Connection aborted, Please try again')
        return render(request, 'service.html')

def serve_edit(request, pk=None):
    serve= get_object_or_404(service, id=pk)
    form = serviceup(request.POST or None, instance=serve)
    username = request.user.username
    activity = "service"+" "+serve.name+" "+"update successfully"
    if form.is_valid():            
            instance=form.save(commit=False)            
            instance.save()
            create = logs.objects.create(activity=activity, user=username)
            messages.success(request, 'Service successfully updated')                
            return redirect('/service/')
    context = {'form':form}
    return render(request, 'service.html', context)

def serve_delete(request, pk):
    servedel= get_object_or_404(service, id=pk)
    if request.method == 'POST':
        servedel.delete()
        return redirect('/service/')
    return render(request, 'service.html')

def employee_regist(request):
    
    if request.method == 'POST':
        name = request.POST["name"]
        contact = request.POST["contact"]
        email = request.POST["email"]
        position = request.POST["position"]
        username = request.user.username
        activity = "employee"+" "+name+" "+"registered successfully"
        
        serve = employee.objects.create(name=name, contact=contact, email=email, position=position, addedby=username)
        create = logs.objects.create(activity=activity, user=username)
        messages.success(request, 'Employee '+name+' successfully registered')
        return redirect('/employees/')
    else: 
        messages.info(request, 'Connection aborted, Please try again')
        return render(request, 'service.html')

def employee_edit(request, pk=None):
    serve= get_object_or_404(employee, id=pk)
    form = employee_up(request.POST or None, instance=serve)
    username = request.user.username
    activity = "employee"+" "+serve.name+" "+"update successfully"
    if form.is_valid():            
            instance=form.save(commit=False)            
            instance.save()
            create = logs.objects.create(activity=activity, user=username)
            messages.success(request, 'Employee successfully updated')                
            return redirect('/employees/')
    context = {'form':form}
    return render(request, 'employees.html', context)

def employee_delete(request, pk):
    empob= get_object_or_404(employee, id=pk)
    username = request.user.username
    activity = "employee"+" "+empob.name+" "+" deleted successfully"
    if request.method == 'POST':
        empob.delete()
        create = logs.objects.create(activity=activity, user=username)
        return redirect('/employee/')
    return redirect('/employees.html/')

@csrf_protect
def cart_reg(request):
    # carto = cart.objects.all()
    if request.method == 'POST':
        service = request.POST["service"]
        service_price = request.POST["service_price"]
        staff = request.POST["staff"]
        username = request.user.username
        activity = "Service "+service+" successfully added to cart"
        
        cart_sub = cart.objects.create(service=service, service_price=service_price, staff=staff, added_by=username)
        create = logs.objects.create(activity=activity, user=username)
        return redirect('/ordermgt/')
    else: 
        messages.info(request, 'Connection aborted, Please try again')
        return redirect('/ordermgt.html/')

def cart_del(request, pk):
    orderup= get_object_or_404(cart, id=pk)
    username = request.user.username
    activity = "service "+orderup.service+" deleted from cart successfully"
    if request.method == 'POST':
        orderup.delete()
        create = logs.objects.create(activity=activity, user=username)
        return redirect('/ordermgt/')
    return redirect('/ordermgt/')

def order_sub(request):
    if request.method == 'POST':
        paid = request.POST["paid"]
        mode = request.POST["mode"]
        customer = request.POST["customer"]
        customer_phone = request.POST["customer_phone"]
        username = request.user.username
        cartobj = cart.objects.filter(added_by=username)
        amount = 0  
        for amt in cartobj: 
            amount = amount+amt.service_price
        order_sub = order.objects.create(customer=customer, mode=mode, customer_phone=customer_phone, amount=amount, paid=paid, balance=int(amount)-int(paid), added_by=username, status=1)    
        for carts in cartobj:
            services = carts.service
            staff = carts.staff   
            service_price = carts.service_price   
            amount = amount+carts.service_price
            comm = service.objects.filter(name=services)[0].commission
            comm_sub = employee.objects.filter(name=staff)[0].commission
            paid_sub = employee.objects.filter(name=staff)[0].paid
            bal_sub = employee.objects.filter(name=staff)[0].balance
            comm_up = employee.objects.filter(name=staff).update(commission=comm_sub+comm)
            bal_up = employee.objects.filter(name=staff).update(balance=(comm_sub+comm)-paid_sub)
            orderdetails = orderdetail.objects.create(staff=staff, service=services, service_price=service_price, order_id=order_sub.id, added_by=username, status=1)
        cartobj.delete()
        activity = "order submission for client "+customer
        create = logs.objects.create(activity=activity, user=username)
        messages.success(request, 'Service Sale has been successfully recorded')
        return redirect('/ordermgt/')
    else: 
        messages.info(request, 'Connection aborted, Please try again')
        return redirect('/ordermgt.html/')



def order_up(request, pk=None):
    orderup= get_object_or_404(order, id=pk)
    username = request.user.username
    activity = "order"+" "+orderup.service+" "+"for"+" "+orderup.items+" "+"has been booked"
    order.objects.filter(id=orderup.id).update(status=1)
    create = logs.objects.create(activity=activity, user=username)   
    messages.success(request, 'order successfully update')             
    return redirect('/ordermgt/')

def order_bo(request, pk=None):
    orderup= get_object_or_404(order, id=pk)
    username = request.user.username
    activity = "order"+" "+orderup.service+" "+"for"+" "+orderup.items+" "+"has been served"
    order.objects.filter(id=orderup.id).update(status=2)
    create = logs.objects.create(activity=activity, user=username)   
    messages.success(request, 'order successfully update')             
    return redirect('/userorder/')
    
def order_del(request, pk):
    orderup= get_object_or_404(order, id=pk)
    username = request.user.username
    activity = "order"+" "+orderup.service+" "+"for"+" "+orderup.items+" "+"deleted successfully"
    if request.method == 'POST':
        orderup.delete()
        create = logs.objects.create(activity=activity, user=username)
        return redirect('/ordermgt/')
    return redirect('/ordermgt/')


    
    








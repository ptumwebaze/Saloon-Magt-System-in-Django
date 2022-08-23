# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from core import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
# from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('admin', admin.site.urls),
    path('service/', views.servepage, name='servepage'),
    path('employees/', views.employeespage, name='employeespage'),    
    path('debt_pays/', views.debt_pays, name='debt_pay'),
    path('client/', views.clientpage, name='clientpage'),
    path('cart/', views.cartpage, name='cartpage'),
    path('debtors/', views.debtors, name='debtors'),
    path('logs/', views.logspage, name='logspage'),
    path('home/', views.homepage, name='homepage'),
    path('orders/', views.orderspage, name='orderspage'),
    path('ordermgt/', views.ordermgt, name='ordermgt'),
    path('userorder/', views.userorder, name='userorder'),
    path('order_add/', views.order_sub, name='order_add'),
    path('ordermgt-up/<int:pk>', views.order_up, name='order_up'),
    path('ordermgt-bo/<int:pk>', views.order_bo, name='order_bo'),
    path('ordermgt/<int:pk>', views.order_del, name='order_del'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cart/<int:pk>', views.cart_del, name='cart_del'),
    path('service-submit/', views.service_regist, name='service_regist'),
    path('service/<int:pk>', views.serve_edit, name='serve_edit'),
    path('service/delete/<int:pk>', views.serve_delete, name='serve_delete'),    
    path('employee-submit/', views.employee_regist, name='employee_regist'),
    path('employee/<int:pk>', views.employee_edit, name='employee_edit'),
    path('employee/delete/<int:pk>', views.employee_delete, name='employee_delete'),
    path('cartadd/', views.cart_reg, name="cartadd"),
    path('cartdel/delete/<int:pk>', views.cart_del, name="cart_del"),
    path('register/', views.register, name="register-sub"),
    path('commissionpage/', views.commissionpage, name="commissionpage"),
    path('commissionpay/', views.commpay, name="commissionpay"),
    path('expense/', views.expenses, name="expenses"),
    path('expense_submit/', views.expense_submit, name="expense_sub"),
    path('expense/<int:pk>/', views.expense_edit, name="expense_edit"),
    path('expense_delete/', views.expense_delete, name="expense_delete"),
    path('sales/', views.salespage, name="sales"),
    path("logout/", LogoutView.as_view(), name="logout"),

]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)




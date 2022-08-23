# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from .models import user_reg
# from .models import cust_reg
from .models import service
from .models import employee
from .models import cart
from .models import order
from .models import orderdetail
from .models import logs

# Register your models here.
admin.site.register(user_reg)
# admin.site.register(cust_reg)
admin.site.register(service)
admin.site.register(employee)
admin.site.register(cart)
admin.site.register(order)
admin.site.register(orderdetail)
admin.site.register(logs)




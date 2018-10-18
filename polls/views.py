# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Orders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
def index(request):
    orders_list = Orders.objects.order_by('trade_date')
    paginator = Paginator(orders_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    index = orders.number - 1 
    max_index = len(paginator.page_range)
    
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'polls/list.html', {'orders': orders, "page_range" : page_range})
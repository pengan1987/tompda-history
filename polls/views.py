# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Orders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
import logging

# Create your views here.


def index(request):
    orders_list = Orders.objects.all()

    page = request.GET.get('page')
    datesort = request.GET.get('sort')
    keyword = request.GET.get('keyword')
    trader = request.GET.get('trader')

    change_order_link = ""
    paging_link_tail = ""
    if trader:
        change_order_link += ("&trader=" + trader)
        paging_link_tail += ("&trader=" + trader)
    if datesort:
        paging_link_tail += ("&sort=" + datesort)
    if keyword:
        change_order_link += ("&keyword=" + keyword)
        paging_link_tail += ("&keyword=" + keyword)
    if page:
        change_order_link += ("&page=" + page)

    change_order_link += "&sort=date_asc" if datesort == 'date_desc' else '&sort=date_desc'
    change_order_link = change_order_link.replace("&", "?", 1)
    logging.warning(change_order_link)

    if trader:
        orders_list = orders_list.filter(Q(buyer__startswith=trader) |
                                         Q(seller__startswith=trader))

    if keyword:
        orders_list = orders_list.filter(item__icontains=keyword)

    if datesort == 'date_desc':
        orders_list = orders_list.order_by('-trade_date')
    else:
        orders_list = orders_list.order_by('trade_date')

    paginator = Paginator(orders_list, 50)

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

    return render(request, 'polls/list.html', {'orders': orders,
                                               "page_range": page_range,
                                               "paging_link_tail": paging_link_tail,
                                               "change_order_link": change_order_link})

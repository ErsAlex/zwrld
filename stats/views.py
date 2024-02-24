
from django.shortcuts import render, get_object_or_404, redirect
from products.models import ItemCategory, Item, Price, PriceHistory, Supply, SoldItemProxy, SoldItem, PayCheck
from urllib.parse import urlencode
from functools import reduce
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import  reverse_lazy, reverse
from django.views.generic import  CreateView, UpdateView, ListView
from stats.forms import SoldItemsDailySearchForm, SoldItemsSearchForm
from django.core.exceptions import PermissionDenied
import datetime
from datetime import date
from stats.filters import sold_item_category_filter, sold_item_filter
from users.security import LoginAndAdminRequiredMixin, login_required_and_superuser
from django.contrib.auth.decorators import login_required



@login_required_and_superuser
def sold_item_stats_range_view(request):
    paginate_by = 10
    url_params = ''
    page = request.GET.get('page')
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1)
    sold_items = SoldItem.objects.select_related("item_in_storage").filter(sale_date__range=[start_date, end_date])
    items = sold_item_filter(sold_items)
    if request.method == 'POST':
        form = SoldItemsSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            sold_items = SoldItem.objects.filter(sale_date__range=[start_date, end_date])
            items = sold_item_filter(sold_items)
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params)
    form = SoldItemsSearchForm()
    paginator = Paginator(items, paginate_by)       
    return render(request, 'stats/sales_main_page.html', context={'items': paginator.get_page(page), "url_params": url_params, "form": form})


@login_required_and_superuser
def sales_by_category_view(request, category):
    paginate_by = 10
    url_params = ''
    page = request.GET.get('page')
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1)
    categories_data = SoldItem.objects.filter(Q(item_category__product_type=category) & Q(sale_date__range=[start_date, end_date]))
    items = sold_item_category_filter(categories_data)
    if request.method == 'POST':
        form = SoldItemsSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            categories_data = SoldItem.objects.filter(Q(item_category__product_type=category) & Q(sale_date__range=[start_date, end_date]))
            items = sold_item_category_filter(categories_data)
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params)
    form = SoldItemsSearchForm()
    paginator = Paginator(items, paginate_by)
    return render(request, 'stats/sales_by_category.html', context={'items': paginator.get_page(page), "url_params": url_params, "form": form})
    
@login_required_and_superuser
def daily_sales_view(request):
    paginate_by = 10
    url_params = ''
    page = request.GET.get('page')
    search_date = date.today()
    item_data = SoldItem.objects.filter(sale_date=search_date)
    if request.method == 'POST':
        form = SoldItemsDailySearchForm(request.POST)
        if form.is_valid():
            search_date = form.cleaned_data['search_date']
            item_data = SoldItem.objects.filter(sale_date=search_date)
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params)
    form = SoldItemsDailySearchForm()
    paginator = Paginator(item_data, paginate_by)
    return render(request, template_name='stats/daily.html', context={'items': paginator.get_page(page), "url_params": url_params, "form": form})
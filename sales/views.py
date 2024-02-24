from django.shortcuts import render, get_object_or_404, redirect
from products.models import ItemCategory, Item, Price, PriceHistory, Supply, SoldItemProxy, SoldItem, PayCheck, SoldWeightItemProxy
from urllib.parse import urlencode
from functools import reduce
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import  reverse_lazy, reverse
from django.views.generic import  CreateView, UpdateView, ListView
from supply.forms import SupplyCreateForm, SupplyUpdateForm
from django.core.exceptions import PermissionDenied
import datetime
from users.security import LoginAndAdminRequiredMixin, login_required_and_superuser
from django.contrib.auth.decorators import login_required
from decimal import Decimal
# Create your views here.


@login_required
def main_page_view(request):
    paginate_by = 12
    page = request.GET.get('page')
    supplies = Supply.objects.filter(supply_checked=True, supply_accepted=False)
    sales = SoldItem.objects.filter(sale_date=datetime.date.today().isoformat())
    unsaved_paychecks = PayCheck.objects.filter(is_issued=False)
    summary_price = 0
    if request.method == "POST":
        req_dict = request.POST.dict()
        if req_dict.get("new_check") == "piece_goods":
            check = PayCheck.objects.create(check_value=0)
            return redirect("sales:paycheck-fill", pk=check.check_id)
        if req_dict.get("new_check") == "weight_goods":
            check = PayCheck.objects.create(check_value=0)
            return redirect("sales:paycheck-fill-weight", pk=check.check_id)
    for item in sales:
        summary_price += item.price
    paginator = Paginator(sales, paginate_by)
    return render(request, template_name="sales/main_page.html", context={"supplies": supplies, "sales": paginator.get_page(page), 'summary': summary_price, "unsaved_paychecks": unsaved_paychecks})


@login_required
def paycheck_creation_detail_piece(request, pk):
    check = get_object_or_404(PayCheck.objects.prefetch_related("proxy_items_in_paycheck"), pk=pk)
    items_in_current_check =  check.proxy_items_in_paycheck.all()
    summary = check.check_value
    if request.method == "POST":
        barcode_dict = request.POST.dict()
        if "delete_paycheck" in barcode_dict:
            if barcode_dict["delete_paycheck"] == "delete":
                items_for_restore = []
                for proxy_item in items_in_current_check:
                    items_for_restore.append(proxy_item.p_item_in_storage)
                for item in items_for_restore:
                    item.in_paycheck = False
                Item.objects.bulk_update(items_for_restore, ["in_paycheck"])
                check.delete()
                return redirect("sales:landing-page")
        
        if barcode_dict.get('delete_item_id') != None:
            delete_item_id = int(barcode_dict['delete_item_id'])
            proxy_sold_item_for_del = SoldItemProxy.objects.get(p_sold_item_id=delete_item_id)
            item_in_storage = proxy_sold_item_for_del.p_item_in_storage
            item_in_storage.in_paycheck = False
            item_in_storage.save()
            proxy_sold_item_for_del.delete()
            check.check_value -= proxy_sold_item_for_del.p_price
            check.save()
            return redirect(request.path)
        if barcode_dict.get("barcode") != '':
            barcode = barcode_dict.get("barcode")
            items = Item.objects.filter(barcode=barcode, is_sold=False, in_store=True, in_paycheck=False)
            if items.exists():
                item = items[0]
                if item.item_category.goods_by_weight == True:
                    return redirect(request.path)
                item.in_paycheck = True
                item.save()
            else:
                item = None
                return redirect(request.path)
            category = item.item_category   
            price = category.price_data.current_price
            p_sold_item = SoldItemProxy(
                p_price = price,
                p_supply_price=item.supply_price,
                p_item_in_storage=item,
                p_item_category=item.item_category,
                p_paycheck=check
                )
            p_sold_item.save()
            check.check_value += p_sold_item.p_price
            check.save()
            summary = check.check_value
            return redirect(request.path)
    return render(request=request, template_name="sales/single_register.html", context={"check": items_in_current_check, "check_id": check.check_id, "summary": summary})


@login_required
def paycheck_save(request, pk):
    paycheck = PayCheck.objects.prefetch_related("proxy_items_in_paycheck").get(check_id=pk)
    payment_type = request.POST.get('payment_type')
    proxy_sold_items = paycheck.proxy_items_in_paycheck.all().prefetch_related('p_item_in_storage')
    sold_items = []
    items_for_update = []
    for proxy_sold_item in proxy_sold_items:
        item = proxy_sold_item.p_item_in_storage
        items_for_update.append(item)
        sold_item = SoldItem(
            price = proxy_sold_item.p_price,
            supply_price=proxy_sold_item.p_supply_price,
            item_in_storage=proxy_sold_item.p_item_in_storage,
            item_category=proxy_sold_item.p_item_category,
            paycheck=paycheck
        )
        sold_items.append(sold_item)
    SoldItem.objects.bulk_create(sold_items)
    
    # исправить для уменьшения кол-ва запросов к БД в цикле.

    for item in items_for_update:
        if item.item_category.goods_by_weight != True:
            item.is_sold = True
            item.in_store = False
    Item.objects.bulk_update(items_for_update, ["is_sold", "in_store"])
    if payment_type:
        type = bool(int(payment_type))
        paycheck.check_cash = type
    paycheck.is_issued = True
    proxy_sold_items.delete()
    paycheck.save()
    return redirect(reverse(viewname='sales:landing-page'))



@login_required
def paycheck_creation_detail_weight(request, pk):
    check = get_object_or_404(PayCheck.objects.prefetch_related("proxy_w_items_in_paycheck"), pk=pk)
    items_in_current_check =  check.proxy_w_items_in_paycheck.all()
    if request.method == "POST":
        barcode_dict = request.POST.dict()
        if "delete_paycheck" in barcode_dict:
            if barcode_dict["delete_paycheck"] == "delete":
                check.delete()
                return redirect("sales:landing-page")
        
        if barcode_dict.get('delete_item_id') != None:
            delete_item_id = int(barcode_dict['delete_item_id'])
            proxy_sold_item_for_del = SoldWeightItemProxy.objects.get(p_sold_item_id=delete_item_id)
            proxy_sold_item_for_del.delete()
            return redirect(request.path)
        
        
        for element in barcode_dict:
            if element.startswith("item_w_id"):
                if barcode_dict.get(element) != None or barcode_dict.get(element) != '':
                    proxy_item_w_id = int(element.split('-')[1])
                    proxy_item_weight = Decimal(barcode_dict.get(element))
                    for item in items_in_current_check:
                        price = item.p_item_category
                        if item.p_sold_item_id == proxy_item_w_id:
                            item.p_weight = proxy_item_weight
        
                            item.p_price = (proxy_item_weight / 100) * item.p_price_data

                            item.save()
                            return redirect(request.path)
        
        
        
        
        
        if barcode_dict.get("barcode") != '':
            barcode = barcode_dict.get("barcode")
            items = Item.objects.filter(barcode=barcode, is_sold=False, in_store=True)
            if items.exists():
                item = items[0]
                if item.item_category.goods_by_weight == False:
                    return redirect(request.path)
            else:
                item = None
                return redirect(request.path)
            category = item.item_category   
            price = category.price_data.current_price
            p_sold_item = SoldWeightItemProxy(
                p_price_data = price,
                p_supply_price=item.supply_price,
                p_item_in_storage=item,
                p_item_category=item.item_category,
                p_paycheck=check
                )
            p_sold_item.save()
            return redirect(request.path)
    summary = 0
    for item in items_in_current_check:
        summary += item.p_price
    check.check_value = summary
    check.save() 
    return render(request=request, template_name="sales/weight_register.html", context={"check": items_in_current_check, "check_id": check.check_id, "summary": summary})


@login_required
def paycheck_weight_save(request, pk):
    paycheck = PayCheck.objects.prefetch_related("proxy_w_items_in_paycheck").get(check_id=pk)
    payment_type = request.POST.get('payment_type')
    proxy_sold_items = paycheck.proxy_w_items_in_paycheck.all().prefetch_related('p_item_in_storage')
    sold_items = []

    for proxy_sold_item in proxy_sold_items:
        sold_item = SoldItem(
            price = proxy_sold_item.p_price,
            supply_price=proxy_sold_item.p_supply_price,
            item_in_storage=proxy_sold_item.p_item_in_storage,
            item_category=proxy_sold_item.p_item_category,
            paycheck=paycheck,
            sold_by_weight=True
        )
        sold_items.append(sold_item)
    SoldItem.objects.bulk_create(sold_items)

    if payment_type:
        type = bool(int(payment_type))
        paycheck.check_cash = type
    paycheck.is_issued = True
    proxy_sold_items.delete()
    paycheck.save()
    return redirect(reverse(viewname='sales:landing-page'))
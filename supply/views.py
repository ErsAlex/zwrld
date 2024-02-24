
from django.shortcuts import render, get_object_or_404, redirect
from products.models import ItemCategory, Item, Price, PriceHistory, Supply
from urllib.parse import urlencode
from functools import reduce
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import  reverse_lazy, reverse
from django.views.generic import  CreateView, UpdateView, ListView
from supply.forms import SupplyCreateForm, SupplyUpdateForm
from django.core.exceptions import PermissionDenied
from users.security import LoginAndAdminRequiredMixin, login_required_and_superuser
from django.contrib.auth.decorators import login_required


@login_required_and_superuser
def supply_approve_view(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    supply.supply_checked = True
    supply.save()
    return redirect(reverse(viewname='supply:supply-detail', kwargs={'pk': pk}))

@login_required_and_superuser
def supply_save_view(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    supply.supply_accepted = True
    supply.save()
    return redirect(reverse(viewname='sales:landing-page'))

# дописать
@login_required
def supply_acceptance_view(request, pk):
    paginate_by = 10    
    supply = get_object_or_404(Supply.objects.prefetch_related("items_in_supply"), pk=pk)
    supply_items = ItemCategory.objects.prefetch_related('price_data').filter(Q(items_in_category__supply=supply))
    supply_items = supply_items.annotate(item_count=Count('items_in_category', filter=Q(items_in_category__supply=supply)))
    supply_items = supply_items.annotate(in_store=Count('items_in_category', filter=Q(items_in_category__in_store=True, items_in_category__supply=supply)))
    page = request.GET.get('page')
    paginator = Paginator(supply_items, paginate_by)
    if request.method == 'POST':
        category_data = request.POST.dict()
        if category_data.get('delete_item_id') != None:
            category_for_cancel_id = category_data.get('delete_item_id')
            category = ItemCategory.objects.get(ItemCategory_id=category_for_cancel_id)
            items = Item.objects.filter(supply=supply, item_category=category)
            for item in items:
                item.barcode = None
                item.in_store = False
                Item.objects.bulk_update(items, ["barcode", "in_store"])
            return redirect(request.path)
        for element in category_data:
            if element.startswith('category-'):
                barcode = category_data[element]
                if barcode == '':
                    return redirect(request.path)
                category_id = int(element.split('-')[1])
                if category_id:
                    category = ItemCategory.objects.get(ItemCategory_id=category_id)
                    items = Item.objects.filter(supply=supply, item_category=category)
                    for item in items:
                        item.barcode = barcode
                        item.in_store = True
                    Item.objects.bulk_update(items, ["barcode", "in_store"])
                    return redirect(request.path)
    return render(request=request, template_name='supply/supply_accept.html', context={"category": paginator.get_page(page), "supply": supply})
    
@login_required_and_superuser
def supply_manger_view(request):
    supplies = Supply.objects.all().order_by('-supply_creation_date')
    paginate_by = 10
    form = SupplyCreateForm()
    page = request.GET.get("page")
    paginator = Paginator(supplies, paginate_by)
    if request.method == 'POST':
        form = SupplyCreateForm(request.POST)
        if form.is_valid():
            supply = form.save()
            return redirect('supply:supply-fill', pk=supply.supply_id)
    
    return render(request, template_name="supply/supply_list.html", context= {"form":form, "supplies" : paginator.get_page(page)})

@login_required_and_superuser
def supply_detail_view(request, pk):
    paginate_by = 10
    page = request.GET.get('page')
    supply = get_object_or_404(Supply.objects.prefetch_related("items_in_supply"), pk=pk)
    paginator = Paginator(supply.items_in_supply.all(), paginate_by)
    if request.method == "POST":
        delete_dict = request.POST.dict()
        delete_item_id = int(delete_dict['delete_item_id'])
        if supply.supply_accepted == True:
            raise PermissionDenied
        item_for_deletion = Item.objects.get(item_id=delete_item_id)
        item_for_deletion.delete()
        return redirect(request.path)
    return render(request, template_name="supply/supply_detail.html",  context={"supply": supply, "items": paginator.get_page(page)})
         
        
@login_required_and_superuser
def supply_create_detail_view(request, pk):
    paginate_by = 10
    url_params = ""    
    supply = get_object_or_404(Supply.objects.prefetch_related("items_in_supply"), pk=pk)
    supply_category_queryset = ItemCategory.objects.all()
    category_search = supply_category_queryset
    if request.method == 'GET':
        sort_by = request.GET.dict()
        if sort_by:
            if sort_by["search-query"] == "":
                if sort_by.get("product_type"):
                    if sort_by["product_type"] != "all":
                        category_search = category_search.filter(Q(product_type=sort_by['product_type']))
                if sort_by.get("pet_type"):     
                    if sort_by["pet_type"] != "all":
                        category_search = category_search.filter(Q(pet_type=sort_by['pet_type']))
            category_search = category_search.filter(Q(name__icontains=sort_by["search-query"]) | Q(description__icontains=sort_by['search-query']) | \
                Q(article__icontains=sort_by['search-query']) | Q(is_dry__icontains=sort_by['search-query']) | Q(brand__icontains=sort_by['search-query'])) 
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params) 
    supply_items = supply_category_queryset.prefetch_related("price_data").filter(Q(items_in_category__supply=supply))
    supply_items = supply_items.annotate(item_count=Count('items_in_category'))
    if request.method == 'POST':
        params_dict = request.POST.dict()
        
        if params_dict.get('delete_item_id') != None: 
            delete_item_category_id = int(params_dict['delete_item_id'])
            delete_item_category = get_object_or_404(ItemCategory, pk=delete_item_category_id)       
            items_for_del = Item.objects.filter(item_category=delete_item_category, supply=supply)
            items_for_del.delete()
            return redirect(request.path)
    
        filtered_data = {}
        creation_data = []
        # этим циклом получаем из реквеста id категории и количество нужный item, кладем в filtered data.
        # Внимание! не будет работать если в POST.dict() category и quantity изменят свой порядок. Осторожно с шаблонами!
        for element in params_dict:
            if element.startswith('category-'):
                category_id = int(element.split('-')[1])
                filtered_data[category_id] = 0
            if element.startswith('quantity-'):
                if params_dict[element] != '':
                    quantity = int(params_dict[element])
                    quantity_id = int(element.split('-')[1])
                    if quantity_id in filtered_data:
                        filtered_data[quantity_id] = quantity
        item_categories = ItemCategory.objects.prefetch_related("price_data").in_bulk(filtered_data.keys())
        # категории и фильтер дата - порядок и значния ключей совпадает
        for cat_id  in filtered_data:
            for n in range(filtered_data[cat_id]):
                model = Item(supply=supply, item_category=item_categories[cat_id], supply_price=item_categories[cat_id].price_data.current_delivery_price)
                creation_data.append(model)
        Item.objects.bulk_create(creation_data)
        
        return redirect(request.path)
    paginator = Paginator(category_search, paginate_by)
    page = request.GET.get('page')             
    return render(request, 'supply/supply_create_detail.html', context={'category': paginator.get_page(page), 'supply': supply, "items_by_category": supply_items, "url_params": url_params})

@login_required_and_superuser
def supply_delete(request, pk):
    supply_for_del = get_object_or_404(Supply, pk=pk)
    supply_for_del.delete()
    return redirect(reverse(viewname='supply:supply-lst'))
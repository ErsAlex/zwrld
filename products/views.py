from django.shortcuts import render, get_object_or_404, redirect
from products.models import ItemCategory, Item, Price, PriceHistory, Supply
from urllib.parse import urlencode
from functools import reduce
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import  reverse_lazy, reverse
from django.views.generic import  CreateView, UpdateView, ListView
from products.forms import ItemCategoryModelForm, ItemCategoryUpdateForm, PriceUpdateForm, PriceCreateForm
from users.security import LoginAndAdminRequiredMixin, login_required_and_superuser
from django.contrib.auth.decorators import login_required
from datetime import date

class CategoryUpdateView(UpdateView, LoginAndAdminRequiredMixin):
    form_class = ItemCategoryUpdateForm
    template_name = 'products/category_update.html'
    queryset = ItemCategory.objects.all()
    
    def get_success_url(self):
        return reverse_lazy('products:category-manager')
    
    
class ItemCategoryCreateView(CreateView, LoginAndAdminRequiredMixin):
    form_class = ItemCategoryModelForm
    template_name = 'products/category_create.html'
    
    def get_success_url(self):
        return reverse_lazy("products:category-manager")

@login_required_and_superuser
def category_manager_view(request):
    paginate_by = 10
    url_params = ""
    page = request.GET.get('page')
    sort_by = request.GET.dict()
    queryset = ItemCategory.objects.all()
    if request.method == 'GET':
        sort_by = request.GET.dict()
        if sort_by:
            if "search-query" not in sort_by or sort_by["search-query"] == "":
                if sort_by.get("product_type"):
                    if sort_by["product_type"] != "all":
                        queryset = queryset.filter(Q(product_type=sort_by['product_type']))
                if sort_by.get("pet_type"):     
                    if sort_by["pet_type"] != "all":
                        queryset = queryset.filter(Q(pet_type=sort_by['pet_type']))
            fields = ['name', 'description', 'article', 'is_dry', 'brand']
            query = sort_by.get('search-query')
            if query:
                queryset = queryset.filter(reduce(lambda x, y: x | y, [Q(**{field + '__icontains': query}) for field in fields]))
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params)
    queryset = queryset.annotate(item_count=Count('items_in_category', filter=Q(items_in_category__is_sold=False, items_in_category__in_store=True)))
    queryset = queryset.prefetch_related('price_data')
    paginator = Paginator(queryset, paginate_by)
    return render(request=request, template_name="products/product_manager.html", context={"category_list": paginator.get_page(page), "url_params": url_params})

@login_required_and_superuser
def category_items_detail(request, pk):
    paginate_by = 10
    page = request.GET.get('page')
    category = get_object_or_404(ItemCategory, pk=pk)
    items = Item.objects.filter(item_category=category, is_sold=False, in_store=True, in_paycheck=False)
    paginator = Paginator(items, paginate_by)
    
    
    if request.method == "POST":
        delete_dict = request.POST.dict()
        
        if delete_dict.get('delete_item_id') != None:
            delete_item_id = int(delete_dict['delete_item_id'])
            item_for_del = Item.objects.get(item_id=delete_item_id)
            item_for_del.delete()
            return redirect(request.path)
    
    return render(request=request, template_name='products/category_detail.html', context={'category': category, 'items': paginator.get_page(page)})

@login_required_and_superuser
def create_price_view(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(ItemCategory, pk=pk)
        form = PriceCreateForm(request.POST)
        if form.is_valid():
            price = Price(
                current_price=form.cleaned_data['current_price'],
                current_delivery_price=form.cleaned_data["current_delivery_price"],
                current_markup=form.cleaned_data["current_markup"],
                current_percent_markup=form.cleaned_data['current_percent_markup'],
                product_category=category
                )
        price.save()
        return redirect(reverse(viewname='products:category-manager'))
    form = PriceCreateForm()
    return render(request, template_name="products/price_create.html", context={'form': form}) 


class PriceHistoryListView(ListView, LoginAndAdminRequiredMixin):
    model = PriceHistory
    template_name = 'products/price_history.html'
    context_object_name = 'price_history_list'

    def get_queryset(self):
        item_category_id = self.kwargs['item_category_id']
        return PriceHistory.objects.filter(new_price__product_category_id=item_category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_category_id = self.kwargs['item_category_id']
        category = ItemCategory.objects.filter(ItemCategory_id=item_category_id)
        context["category"] = category[0]
        return context
        
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('page')
        context['category_list'] = paginator.get_page(page)
        return context        

@login_required_and_superuser
def price_history_view(request, pk):
    paginate_by = 10
    page = request.GET.get('page')
    category = get_object_or_404(ItemCategory, pk=pk)
    current_price = Price.objects.get(product_category=category)
    price_list = PriceHistory.objects.filter(new_price=current_price)
    paginator = Paginator(price_list, paginate_by)
    return render(request=request, template_name='products/price_history.html', context={'price_history_list': paginator.get_page(page)})
    
   


@login_required_and_superuser
def price_update_view(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(ItemCategory, pk=pk)
        price = Price.objects.get(product_category=category)
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            price_history = PriceHistory(
            old_price=price.current_price,
            delivery_price=price.current_delivery_price,
            markup=price.current_markup,
            percent_markup=price.current_percent_markup,
            new_price=price
        )
        price_history.save()
        price.current_price = form.cleaned_data['current_price']
        price.current_delivery_price = form.cleaned_data["current_delivery_price"]
        price.current_markup = form.cleaned_data["current_markup"]
        price.current_percent_markup = form.cleaned_data['current_percent_markup']
        price.save()
        return redirect('products:category-manager')
    form = PriceUpdateForm()
    return render(request=request, template_name="products/price_update.html", context={'form': form})



@login_required_and_superuser
def item_create(request):
    paginate_by = 10
    url_params = ""
    page = request.GET.get('page')
    sort_by = request.GET.dict()
    queryset = ItemCategory.objects.all()
    if request.method == 'GET':
        sort_by = request.GET.dict()
        if sort_by:
            if "search-query" not in sort_by or sort_by["search-query"] == "":
                if sort_by.get("product_type"):
                    if sort_by["product_type"] != "all":
                        queryset = queryset.filter(Q(product_type=sort_by['product_type']))
                if sort_by.get("pet_type"):     
                    if sort_by["pet_type"] != "all":
                        queryset = queryset.filter(Q(pet_type=sort_by['pet_type']))
            fields = ['name', 'description', 'article', 'is_dry', 'brand']
            query = sort_by.get('search-query')
            if query:
                queryset = queryset.filter(reduce(lambda x, y: x | y, [Q(**{field + '__icontains': query}) for field in fields]))
            params = request.GET.copy()
            params.pop('page', None)
            url_params = urlencode(params)
    queryset = queryset.annotate(item_count=Count('items_in_category', filter=Q(items_in_category__is_sold=False, items_in_category__in_store=True)))
    queryset = queryset.prefetch_related('price_data')
    paginator = Paginator(queryset, paginate_by)
    if request.method == 'POST':
        params_dict = request.POST.dict()

        quantity, barcode, category_id = int(params_dict.get('quantity')), params_dict.get('barcode'), int(params_dict.get('category'))
        category = ItemCategory.objects.prefetch_related('price_data').get(ItemCategory_id=category_id)
        revision_supply = Supply.objects.filter(revision_supply=True)
        if not revision_supply:
                revision_supply = Supply(
                    supply_creation_date=date.today(),
                    supply_delivery_date=date.today(),
                    supply_checked=True,
                    supply_accepted=True,
                    revision_supply=True,
                    supply_name='Ревизия'
                )
                revision_supply.save()
        else:
            revision_supply = revision_supply[0]
        model_lst = []
        for n in range(quantity):
            model = Item(
                barcode=barcode,
                in_store=True,
                supply_price=category.price_data.current_delivery_price,
                item_category=category,
                supply=revision_supply
                )
            model_lst.append(model)
        Item.objects.bulk_create(model_lst)
        return redirect(request.path)
    return render(request=request, template_name="products/revision.html", context={"category": paginator.get_page(page), "url_params": url_params})


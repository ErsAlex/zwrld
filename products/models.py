
from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime



class ItemCategory(models.Model):
    
    class Product_type(models.TextChoices):
        FOOD = "FOOD", "food"
        SNACKS = "SNACKS", "snacks"
        LITTER = "LITTER", "litter"
        TOYS = "TOYS", "toys"
        MEDECINE = "MEDECINE", "medecine"
        GROOMING = "GROOMING", "grooming"
        OTHER = "OTHER", "other"
        
    class Pet_type(models.TextChoices):
        CATS = "CATS", "cats"
        DOGS = "DOGS", "dogs"
        RODENTS = "RODENTS", "rodents"
        FISH = "FISH", "fish"
        BIRDS = "BIRDS", "birds"
        MULTIPLE = "MULTIPLE", "multiple"
        OTHER = "OTHER", "other"
        
    class Importance_Degree(models.TextChoices):
        MUST = "MUST", "must"
        HIGH_DEMAND = "HIGH_DEMAND", 'high_demand'
        AVERAGE =  "AVERAGE", "Average"
        NOT_IMPORTANT = "NOT_IMPORTANT", "not_important"
        
                
    ItemCategory_id = models.AutoField(primary_key=True)
    article = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    product_type = models.CharField(max_length=15, choices=Product_type.choices)
    pet_type = models.CharField(max_length=15, choices=Pet_type.choices)
    brand = models.CharField(max_length=50, default="brand")
    weight = models.IntegerField(null=False, blank=False, default=1)
    is_dry  = models.BooleanField(default=True, null=True)
    importance = models.CharField(max_length=15, choices=Importance_Degree.choices)
    planned_amount = models.IntegerField(null=False, blank=False, default=0)
    yellowzone_high_border = models.IntegerField(null=True, blank=True)
    yellowzone_low_border = models.IntegerField(null=True, blank=True)
    goods_by_weight = models.BooleanField(default=False)
    
    @property
    def goods_by_weight_str(self):
        if self.goods_by_weight == False:
            return "Штучный"
        return "На развес"
    
    @goods_by_weight_str.setter
    def goods_by_weight_str(self):
        pass
    
    @property
    def importance_str(self):
        if self.importance in ["MUST", "must"]:
            importance_type = "Обязательно в наличии"
        if self.importance in ["HIGH_DEMAND", 'high_demand']:
            importance_type = "Большой спрос"
        if self.importance in ["AVERAGE", "Average"]:
            importance_type = "Средний спрос"
        if self.importance in ["NOT_IMPORTANT", "not_important"]:
            importance_type = "Необязательно в наличии"
        return importance_type
    
    @importance_str.setter
    def importance_str(self):
        pass
    
    @property
    def description_str(self):
        if self.description != None:
            return self.description
        return ""
        
    @description_str.setter
    def description_str(self):
        pass
    
    # переписать нормально
    @property
    def product_type_str(self):
        if self.product_type in ["FOOD", "food"]:
            item_type = "Корм"
        if self.product_type in ["SNACKS", "snacks"]:
            item_type = "Вкусняшка"
        if self.product_type in ["LITTER", "litter"]:
            item_type = "Наполнитель"
        if self.product_type in ["TOYS", "toys"]:
            item_type = "Игрушки и Акссесуары"
        if self.product_type in ["MEDECINE", "medecine"]:
            item_type = "Медицина"
        if self.product_type in ["GROOMING", "grooming"]:
            item_type = "Красота и здоровье"
        if self.product_type in ["OTHER", "other"]:
            item_type = "Другое"
        return item_type
    
    @product_type_str.setter
    def product_type_str(self):
        pass
    
    @property
    def dry_type_str(self):
        dr_type = 'Нет'
        if self.is_dry == True:
            dr_type = "Cухой"
        elif self.is_dry == False:
            dr_type = "Жидкий"
        return dr_type
    
    @dry_type_str.setter
    def dry_type_str(self):
        pass
    # переписать нормально
    @property
    def pet_type_str(self):
        pet_name = self.pet_type
        if self.pet_type in ["CATS", "cats"]:
            pet_name = "Кошки"
        elif self.pet_type in ["DOGS", "dogs"]:
            pet_name = "Собаки"
        elif self.pet_type in ["RODENTS", "rodents"]:
            pet_name = "Грызуны"
        elif self.pet_type in ["FISH", "fish"]:
            pet_name = "Рыбы"
        elif self.pet_type in ["BIRDS", "birds"]:
            pet_name = "Птицы"
        elif self.pet_type in ["MULTIPLE", "multiple"]:
            pet_name = "Разные"
        return pet_name
    
    @pet_type_str.setter
    def pet_type_str(self):
        pass
    
    @property
    def weight_str(self):
        if self.weight == 1:
            return ""
        return self.weight
    
    @weight_str.setter
    def weight_str(self):
        pass
    
    @property
    def brand_str(self):
        if self.brand == "brand":
            return ''
        return self.brand
    
    @brand_str.setter
    def brand_str(self):
        pass
    
    @property
    def is_dry_str(self):
        if self.is_dry != None:
            return self.is_dry
        return ''
    
    @is_dry_str.setter
    def is_dry_str(self):
        pass
    
        
    #перепсать нормально
    def __str__(self):
        pet_name_str = self.pet_type
        if self.pet_type in ["CATS", "cats"]:
            pet_name_str = "кошек"
        elif self.pet_type in ["DOGS", "dogs"]:
            pet_name_str = "собак"
        elif self.pet_type in ["RODENTS", "rodents"]:
            pet_name_str = "грызунов"
        elif self.pet_type in ["FISH", "fish"]:
            pet_name_str = "рыб"
        elif self.pet_type in ["BIRDS", "birds"]:
            pet_name_str = "птиц"
        elif self.pet_type in ["MULTIPLE", "multiple"]:
            return f'{self.brand} {self.name}'
        return f'{self.brand} {self.name} для {pet_name_str} {self.description}'


class Price(models.Model):
    price_id = models.AutoField(primary_key=True)
    current_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    current_delivery_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    current_markup = models.DecimalField(default=0, null=False,blank=False, max_digits=8, decimal_places=2)
    current_percent_markup = models.IntegerField(default=0, null=False, blank=False)
    product_category = models.OneToOneField(ItemCategory, on_delete=models.CASCADE, related_name="price_data")
    
    def __str__(self):
        return f'номер: {self.price_id} продукт: {self.product_category} текущая цена: {self.current_price} текущая цена поставки: {self.current_delivery_price} текущая наценка: {self.current_markup}'
    
class PriceHistory(models.Model):
    price_history_id = models.AutoField(primary_key=True)
    change_date =models.DateTimeField(default=timezone.now, null=True, blank=True)
    old_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    delivery_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    markup = models.DecimalField(default=0, null=False,blank=False, max_digits=8, decimal_places=2)
    percent_markup = models.IntegerField(default=0, null=False, blank=False)
    new_price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name="price_history")
    
    def __str__(self):
        return f'номер: {self.price_history_id} дата изменения: {self.change_date} цена: {self.old_price} цена поставки: {self.delivery_price} наценка: {self.markup} новая цена: {self.new_price}'
    

class Supply(models.Model):
    supply_id = models.AutoField(primary_key=True)
    supply_creation_date = models.DateTimeField(default=timezone.now)
    supply_delivery_date = models.DateField()
    supply_name = models.CharField(max_length=50, null=False, blank=False)
    supply_checked = models.BooleanField(default=False)
    supply_accepted = models.BooleanField(default=False, null=False, blank=False)
    revision_supply = models.BooleanField(default=False)
    
    @property
    def supply_checked_str(self):
        if self.supply_checked != True:
            return f'Поставка не утверждена'
        return f'Утверждена'
    
    @supply_checked_str.setter
    def supply_checked_str(self):
        pass
    
    @property
    def supply_accepted_str(self):
        if self.supply_accepted != True:
            return f'В пути'
        return f'Принята'
    
    @supply_accepted_str.setter
    def supply_accepted_str(self):
        pass
    
    def get_create_url(self):
        return reverse('products:supply-fill', kwargs={'pk':self.supply_id})

    def __str__(self):
        return f'номер {self.supply_id} создана:{self.supply_creation_date} дата поставки: {self.supply_delivery_date}'
    
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50)
    supply = models.ManyToManyField(Supply, related_name="supplier_data")

    def __str__(self):
        return f'номер: {self.supplier_id} поставщик:{self.supplier_name}'

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    barcode = models.CharField(null=True, blank=True, max_length=20)
    in_store  = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    in_paycheck = models.BooleanField(default=False)
    sale_date = models.DateTimeField(null=True, blank=True)
    supply_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="items_in_category")
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name="items_in_supply")
    
    def __str__(self):
        return f'номер: {self.item_id} штрих-код: {self.barcode} категория: {self.item_category}'
    
    @property
    def  in_store_str(self):
        if self.in_store == True:
            return f'В магазине'
        return f'Отсутствует'
    
    @in_store_str.setter
    def in_store_str(self):
        pass
    @property
    def is_sold_str(self):
        if self.is_sold == True:
            return f'Продан'
        return f'Не продан' 
    
    @is_sold_str.setter
    def is_sold_str(self):
        pass

    @property
    def sale_date_str(self):
        if not self.sale_date:
            return ""
        return self.sale_date
    
    
    @sale_date_str.setter
    def sale_date_str(self):
        pass
    
class PayCheck(models.Model):
    check_id = models.AutoField(primary_key=True)
    check_date = models.DateField(default=datetime.datetime.now)
    check_value = models.DecimalField(null=False, blank=False, max_digits=8, decimal_places=2)
    check_cash = models.BooleanField(default=False)
    is_issued = models.BooleanField(default=False)
    
    
    @property
    def check_cash_str(self):
        if self.check_cash == False:
            return "Безнал."
        return f'Наличные'
    
    @check_cash_str.setter
    def check_cash_str(self):
        pass 
        
       
    def __str__(self):
        if self.check_cash == False: 
            return f'номер: {self.check_id} дата: {self.check_date} сумма: {self.check_value} оплата: Безнал.'
        return f'номер: {self.check_id} дата: {self.check_date} сумма: {self.check_value} оплата: Нал.' 
    
class SoldItemProxy(models.Model):
    p_sold_item_id = models.AutoField(primary_key=True)
    p_price = models.DecimalField(null=False, blank=False, max_digits=8, decimal_places=2)
    p_supply_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    p_percent_discount = models.IntegerField(default=0)
    p_item_in_storage = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="proxy_sell_data")
    p_item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="proxy_sold_item_in_category")
    p_paycheck = models.ForeignKey(PayCheck, on_delete=models.CASCADE, related_name="proxy_items_in_paycheck")
    
    
class SoldWeightItemProxy(models.Model):
    p_sold_item_id = models.AutoField(primary_key=True)
    p_weight = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    p_price = models.DecimalField(null=False, blank=False, max_digits=8, decimal_places=2, default=0)
    p_price_data = models.DecimalField(null=False, blank=False, max_digits=8, decimal_places=2, default=0)
    p_supply_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    p_percent_discount = models.IntegerField(default=0)
    p_item_in_storage = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="proxy_w_sell_data")
    p_item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="proxy_w_sold_item_in_category")
    p_paycheck = models.ForeignKey(PayCheck, on_delete=models.CASCADE, related_name="proxy_w_items_in_paycheck")

class SoldItem(models.Model):
    sold_item_id = models.AutoField(primary_key=True)
    sale_date = models.DateField(default=datetime.datetime.now)
    price = models.DecimalField(null=False, blank=False, max_digits=8, decimal_places=2)
    supply_price = models.DecimalField(default=0, null=False, blank=False, max_digits=8, decimal_places=2)
    percent_discount = models.IntegerField(default=0)
    item_in_storage = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="sell_data")
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="sold_item_in_category")
    paycheck = models.ForeignKey(PayCheck, on_delete=models.CASCADE, related_name="items_in_paycheck")
    sold_by_weight = models.BooleanField(default=False)
    
    @property
    def sold_by_weight_str(self):
        if self.sold_by_weight == False:
            return "Штучный"
        return "На развес"
    
    @sold_by_weight_str.setter
    def sold_by_weight_str(self):
        pass
    
    def __str__(self):
        return f'номер: {self.sold_item_id} дата: {self.sale_date} цена: {self.price}'
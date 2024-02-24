from django import forms
from products.models import ItemCategory, Price

class ItemCategoryModelForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = [
            "article",
            "name",
            "description",
            "product_type",
            'pet_type',
            "brand",
            "weight",
            "is_dry",
            'importance',
            'planned_amount',
            'yellowzone_high_border',
            'yellowzone_low_border',
            'goods_by_weight'
        ]

class ItemCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = [
            "name",
            'article',
            "description",
            "product_type",
            "pet_type",
            "brand",
            "weight",
            "is_dry",
            'importance',
            'planned_amount',
            'yellowzone_high_border',
            'yellowzone_low_border',
            'goods_by_weight'
                  
        ]
        
     
        
class PriceUpdateForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = [
            "current_price",
            "current_delivery_price",
            "current_markup",
            'current_percent_markup'
        ]
 
class PriceCreateForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = [
            "current_price",
            "current_delivery_price",
            "current_markup",
            'current_percent_markup'
        ]
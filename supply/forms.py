from django import forms
from products.models import Supply
from django.forms import DateInput



class SupplyCreateForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields =[
        'supply_delivery_date',
        'supply_name',
    ]
        widgets = {"supply_delivery_date": forms.widgets.DateInput(attrs={'type': 'date'}), "supply_name": forms.widgets.TextInput(attrs={"placeholder": "Название"})}
 

    
class SupplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields =[
        'supply_delivery_date',
        'supply_name',
    ]
    
    def __init__(self, *args, **kwargs):

            super(SupplyUpdateForm, self).__init__(*args, **kwargs)
            self.fields['supply_delivery_date'] = DateInput()

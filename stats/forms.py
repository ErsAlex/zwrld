from django import forms






class SoldItemsSearchForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class SoldItemsDailySearchForm(forms.Form):
    search_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
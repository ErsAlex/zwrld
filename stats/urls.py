from django.urls import path
from stats.views import  daily_sales_view, sold_item_stats_range_view, sales_by_category_view


app_name = "stats"

urlpatterns = [
    path('sales/daily/', daily_sales_view, name='sales-daily'),
    path('sales/<str:category>/', sales_by_category_view, name='sales-category'),
    path('sales/', sold_item_stats_range_view, name='sales-main'),

]
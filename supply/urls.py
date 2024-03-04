
from django.urls import path
from supply.views import  supply_manger_view, supply_create_detail_view, supply_delete, supply_acceptance_view, supply_detail_view, supply_approve_view,supply_save_view, add_items_to_supply, delete_item_from_supply

app_name = "supply"

urlpatterns = [ 
    path('main/', supply_manger_view, name='supply-lst'),
    path('<int:pk>/filling/',supply_create_detail_view, name='supply-fill'),
    path('<int:pk>/detail/',supply_detail_view, name='supply-detail'),
    path('<int:pk>/approve/',supply_approve_view, name='supply-approve'),
    path('<int:pk>/accept/',supply_acceptance_view, name='supply-accept'),
    path('<int:pk>/save/',supply_save_view, name='supply-save'),
    path('<int:pk>/delete/',supply_delete, name='supply-delete'),
    path('<int:pk>/additem/<int:category_id>', add_items_to_supply, name='supply-additem'),
    path('<int:pk>/delitem/', delete_item_from_supply, name='supply-del-item'),
]
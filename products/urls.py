from django.urls import path
from products.views import  PriceHistoryListView, CategoryUpdateView, \
    ItemCategoryCreateView, create_price_view, category_manager_view, category_items_detail, price_update_view, price_history_view, item_create, add_items_to_category



app_name = "products"


urlpatterns = [
    path('manager/', category_manager_view, name='category-manager'),
    path('items/<int:pk>', category_items_detail, name='category-storage'),
    path('category/create/', ItemCategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/price_history/', price_history_view, name='price-list'),
    path("category/<int:pk>/prices/create", create_price_view, name='price-create'),
    path('category/prices/<int:pk>/update/', price_update_view, name='price-update'),
    path('category/revision/', item_create, name='revision'),
    path('category/<int:pk>/additem/', add_items_to_category, name='add-item'),
]
    
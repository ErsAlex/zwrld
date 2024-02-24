from django.urls import path
from sales.views import  paycheck_creation_detail_piece, paycheck_save, main_page_view, paycheck_creation_detail_weight, paycheck_weight_save



app_name = "sales"

urlpatterns = [
    path("", main_page_view, name='landing-page'),
    path('paycheck/<int:pk>/filling/', paycheck_creation_detail_piece, name="paycheck-fill"),
    path('paycheck/<int:pk>/filling-weight/', paycheck_creation_detail_weight, name="paycheck-fill-weight"),
    path('paycheck/<int:pk>/save/', paycheck_save, name="paycheck-save"),
    path('paycheck/<int:pk>/save-weight/', paycheck_weight_save, name="paycheck-save-weight"),
]
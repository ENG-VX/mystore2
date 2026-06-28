from django.urls import path
from . import views

urlpatterns = [
    path("products/",views.product_list),
    path("products/<int:id>/",views.product_detail),

    path("collections/", views.collection_list),
    path("collections/<int:pk>/",views.collection_detail, name='collection-detail'),
    
    path("order/",views.Order_list),
    path("order/<int:id>",views.Order_detail),
    path("customer/<int:pk>",views.customer_detail, name="customer-information")
]
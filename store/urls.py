from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls
urlpatterns = [
    path('',include(router.urls)),
    path('', include(product_router.urls))
    # path("products/",views.ProductList.as_view()),
    # path("products/<int:pk>/",views.ProductDetails.as_view()),

    # path("collections/", views.CollectionList.as_view()),
    # path("collections/<int:pk>/",views.CollectionDetail.as_view(), name='collection-detail'),
    
    # path("order/",views.Order_list),
    # path("order/<int:id>",views.Order_detail),
    # path("customer/<int:pk>",views.customer_detail, name="customer-information")
]
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
    # from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from .filters import *

# Create your views by class way (still not the best way), because you using OOP features
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}

    # if you have some logic use them
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    # def get_serializer(self, *args, **kwargs):
    #     return ProductSerializer
    



# Create your views by functional way (not best way)
# @api_view(['POST', 'GET'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').order_by('id')[:10]
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# first way to get obj and handel it if it not found
# @api_view()
# def product_detail(request,id):   
#     try:
#         product = Product.objects.get(id = id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status.HTTP_404_NOT_FOUND)


# second and bitter way to get obj and handel it if it not found
# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'errrrrror':"product can't be deleted because it linked with order item" },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price','last_update']


    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'errrrrror':"product can't be deleted because it linked with order item" },status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    





class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(number_of_products=Count('product')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).exists():
            return Response({'error':'You can not delete this collection because it has some products'})
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
  
        

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view()
def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)
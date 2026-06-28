from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *

# Create your views by class way (the best way), because you using OOP features
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').order_by('id')[:10]
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetails(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'errrrrror':"product can't be deleted because it linked with order item" },status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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



@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(number_of_products=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    

@api_view(['GET','POST','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(Collection.objects.annotate(number_of_products=Count('product')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'POST':
        collection = CollectionSerializer(Collection, request.data)
        collection.is_valid(raise_exception=True)
        collection.save()
        return Response(collection.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if collection.number_of_products>0:
            return Response({'error':'You can not delete this collection because it has some products'})
        else:
            collection.delete()
            return Response(collection.data, status=status.HTTP_204_NO_CONTENT)



@api_view()
def Order_list(request):
    queryset = Order.objects.all()
    serializer = OrderSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def Order_detail(request, id):
    order = Order.objects.get(pk=id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view()
def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)
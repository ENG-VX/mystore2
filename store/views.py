from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
@api_view(['POST', 'GET'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').order_by('id')[:10]
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
@api_view(['GET','PUT'])
def product_detail(request,id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view()
def collection_detail(request, pk):
    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)

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
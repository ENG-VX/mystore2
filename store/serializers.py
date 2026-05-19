from rest_framework import serializers
from decimal import Decimal
from .models import *

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calc_price_with_tax')
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )
    

    def calc_price_with_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 255)
    last_name = serializers.CharField(max_length = 255)

class OrderSerializer(serializers.Serializer):
    date = serializers.DateTimeField(source = 'placed_at')
    payment_status = serializers.CharField(max_length = 255)
    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(), view_name='customer-information'
    )
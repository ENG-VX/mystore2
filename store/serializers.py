from rest_framework import serializers
from decimal import Decimal
from .models import *

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'inventory', 'description', 'unit_price', 'collection','price_with_tax']

    # to valid in a different way
    # def validate(self, data):
    #     if data['pass'] != data['conf_pass']:
    #         return serializers.ValidationError('password not match')
    #     return data

    # to add some modification on the data before saving it (and we have the same for update method)
    # def save(self, **kwargs):
    #     product = Product(**kwargs)
    #     product.newField = 1
    #     product.save()
    #     return product
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calc_price_with_tax')
    # # collection = serializers.StringRelatedField()
    # # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    

    def calc_price_with_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['first_name', 'last_name']
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['date', 'payment_status', 'customer']
    payment_status = serializers.CharField(max_length = 255)
    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(), view_name='customer-information'
    )
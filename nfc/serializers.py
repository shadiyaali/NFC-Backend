from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'  
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
     
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
       
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        return super().update(instance, validated_data)

 
class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = '__all__'  

 

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class UsersListSerializer(serializers.ModelSerializer): 
    template = TemplateSerializer(read_only=True)  
    vendor =  VendorSerializer(read_only=True)  
    class Meta:
        model = Users
        fields = '__all__'  

 

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class SubscribersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscribers
        fields = '__all__'


class SubscribersListSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True) 
    plan = SubscriptionSerializer(read_only=True) 
    class Meta:
        model = Subscribers
        fields = '__all__'


class ReceivableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Receivables
        fields = '__all__'

 

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'


 
 

from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password, make_password




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

 
 

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['id', 'url']

class UsersSerializer(serializers.ModelSerializer):
    social_media_links = SocialMediaLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Create the user object
        user = Users.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # Update the user object
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UsersListSerializer(serializers.ModelSerializer): 
   
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



 
class VendorPasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password must match.")
        return data
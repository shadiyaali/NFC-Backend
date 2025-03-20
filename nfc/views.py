from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import *
from .serializers import *
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

import base64
import json
from django.core.files.base import ContentFile
 
 
  

User = get_user_model()



class AdminLogin(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password) and user.is_staff and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

 
class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
 

class UsersListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
    def create(self, request, *args, **kwargs):    
        print("request data:", request.data)

        data = request.data.copy()

       
        social_media_links = []
        if 'social_media_links' in data:
            try:
                social_media_links = json.loads(data.get('social_media_links', '[]'))
                data.pop('social_media_links')
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format for social_media_links"}, status=status.HTTP_400_BAD_REQUEST)

  
        profile_image = data.get("profile_image")
        if profile_image and profile_image.startswith("data:image"):
            try:
                format, imgstr = profile_image.split(';base64,')
                ext = format.split('/')[-1]
                img_data = ContentFile(base64.b64decode(imgstr), name=f"profile.{ext}")
                data["profile_image"] = img_data  
            except Exception as e:
                return Response({"error": "Invalid image format"}, status=status.HTTP_400_BAD_REQUEST)

     
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        
        for link in social_media_links:
            if link and isinstance(link, str):
                SocialMediaLink.objects.create(user=user, url=link)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        social_links = []   
        if 'social_media_links' in data:
            import json
            try:
                social_links = json.loads(data.get('social_media_links', '[]'))
                data.pop('social_media_links')
            except:
                pass
        data['social_links'] = social_links       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

 
class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

 
class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SubscribersListCreateView(generics.ListCreateAPIView):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer

 
class SubscribersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersListSerializer

class ReceivablesCreateView(generics.ListCreateAPIView):
    queryset = Receivables.objects.all()
    serializer_class = ReceivableSerializer

 
class ReceivablesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receivables.objects.all()
    serializer_class = ReceivableSerializer

 
class ExpensesCreateView(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

 
class ExpensesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer




class VendorLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor = Vendor.objects.get(username=username)
        except Vendor.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, vendor.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if vendor.status != 'Active':
            return Response({"error": "Your account is blocked"}, status=status.HTTP_403_FORBIDDEN)

        
        refresh = RefreshToken()
        refresh.payload.update({
            "user_id": vendor.id,  
            "username": vendor.username,  
            "token_type": "refresh"
        })

        access = refresh.access_token
        access.payload.update({
            "user_id": vendor.id,
            "username": vendor.username,
            "token_type": "access"
        })

        return Response({
            "access": str(access),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class VendorPasswordUpdateView(APIView):

    def post(self, request, pk):   
        try:
            vendor = Vendor.objects.get(pk=pk)   
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorPasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')
            confirm_password = serializer.validated_data.get('confirm_password')

            if new_password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            vendor.set_password(new_password)
            vendor.save()

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



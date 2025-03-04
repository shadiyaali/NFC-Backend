from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth.hashers import check_password

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

 
class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersListSerializer

class TemplateListCreateView(generics.ListCreateAPIView):
    queryset = Templates.objects.all()
    serializer_class = TemplateSerializer

 
class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Templates.objects.all()
    serializer_class = TemplateSerializer


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


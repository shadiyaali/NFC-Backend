from django.urls import path
from .views import *

urlpatterns = [
    path('login/',AdminLogin.as_view(), name='admin_login'),
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('users/', UsersListCreateView.as_view(), name='users-list-create'),  
    path('users/<int:pk>/', UsersDetailView.as_view(), name='users-detail'),  
    path('templates/', TemplateListCreateView.as_view(), name='template-list-create'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'), 
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),   
    path('subscribers/', SubscribersListCreateView.as_view(), name='subscribers-list-create'),  
    path('subscribers/<int:pk>/', SubscribersDetailView.as_view(), name='subscribers-detail'), 
    path('receivable/', ReceivablesCreateView.as_view(), name='subscribers-list-create'),  
    path('receivable/<int:pk>/', ReceivablesDetailView.as_view(), name='subscribers-detail'), 
    path('expenses/', ExpensesCreateView.as_view(), name='expenses-list-create'),
    path('expenses/<int:pk>/', ExpensesDetailView.as_view(), name='expenses-detail'),
    path('vendor/login/', VendorLoginView.as_view(), name='vendor-login'),
]
 
 
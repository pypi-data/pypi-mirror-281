from django.shortcuts import render
from rest_framework import generics
from customers.models import Client, Domain
from django.conf import settings
from .serializers import CreateTenantSerializer
# Create your views here.


class CreateTenantView(generics.CreateAPIView):
    """view for creating new tenant."""
    serializer_class = CreateTenantSerializer

    def create_domain(self,domain_url,serializer):
        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = domain_url# don't add your port or www here!
        domain.tenant = serializer.data
        domain.is_primary = True
        domain.save()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.create_domain(data.get('domain'),serializer)
        

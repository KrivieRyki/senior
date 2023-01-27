from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import viewsets

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client', queryset = Client.objects.all().select_related('user').only('company_name','user__email'))
    )
    serializer_class = SubscriptionSerializer


from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch, Sum
from rest_framework import viewsets

from clients.models import Client
from services.models import Subscription, Plan
from services.serializers import SubscriptionSerializer, PlanSerializer


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('Plan',
                                                           Prefetch('client',
                                                                    queryset=Client.objects.all().select_related(
                                                                        'user').only('company_name', 'user__email'))
                                                           )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)
        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)
        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data
        return response


class PlanView(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

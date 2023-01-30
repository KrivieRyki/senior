from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    Plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return instance.price
    #
    # def get_price (self, instance):
    #     return instance.service.full_price - instance.service.full_price * (instance.Plan.discount_percent / 100)

    class Meta:
        model = Subscription
        fields = '__all__'

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ['imagen']

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/producto/{obj.id}/")
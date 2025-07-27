from rest_framework import serializers

from infrastructure.persistence.models.catalog.product_type import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name"]

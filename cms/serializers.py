from rest_framework import serializers

from .get_component import get_component
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    components = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "components")

    def get_components(self, page):
        components = [get_component(component.name) for component in page.components.all()]

        for component in components:
            component.template.file = "cms/" + component.template.file

        return components

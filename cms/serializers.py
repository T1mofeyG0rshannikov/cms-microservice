from rest_framework import serializers

from .models import Page


class PageSerializer(serializers.ModelSerializer):
    components = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "components")

    def get_components(self, page):
        components = [
            component["component"] for component in ComponentSerializer(page.components.all(), many=True).data
        ]

        return components


class ComponentSerializer(serializers.Serializer):
    component = serializers.SerializerMethodField()

    def get_component(self, base_component):
        component = None
        if base_component.excomponent.first() is not None:
            component = base_component.excomponent.first()

        elif base_component.navcomponent.first() is not None:
            component = base_component.navcomponent.first()

        component.template = "cms/" + component.template

        return component

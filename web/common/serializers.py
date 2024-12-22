from rest_framework import serializers


class DateFieldDot(serializers.Field):
    def to_representation(self, value):
        return value.strftime("%d.%m.%Y")


class ImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.url

        return ""

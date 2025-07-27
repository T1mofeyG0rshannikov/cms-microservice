from django import forms
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat

from infrastructure.persistence.models.blocks.common import BaseBlock, Block
from infrastructure.persistence.models.utils import get_model_class_by_str


class PageBlockInlineForm(forms.ModelForm):
    custom_name = forms.ChoiceField(label="Блок")

    class Meta:
        model = Block
        fields = ["custom_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queries = []
        for model in apps.get_models():
            if issubclass(model, BaseBlock) and model != BaseBlock:
                queries.append(
                    model.objects.annotate(
                        value=Concat(Value(model.__name__), Value(";"), F("id"), output_field=CharField())
                    )
                    .order_by("name")
                    .values("value", "name"),
                )

        while len(queries) > 1:
            queries[1] = queries[1].union(queries[0])
            queries = queries[1::]

        query = queries[0]
        results = list(query)

        initial = None
        for r in results:
            try:
                if r["name"] == str(self.instance):
                    initial = (r["value"], r["name"])
            except:
                pass
        self.fields["custom_name"].choices = [(r["value"], r["name"]) for r in results]
        self.fields["custom_name"].initial = initial

    def clean_custom_name(self):
        return self.cleaned_data["custom_name"]

    def save(self, commit=True):
        obj = super().save(commit=commit)
        block_class = None
        block_class_name, block_id = self.cleaned_data["custom_name"].split(";")
        block_class = get_model_class_by_str(block_class_name)
        block_content_type = ContentType.objects.get_for_model(block_class)

        obj.content_type = block_content_type
        obj.block_id = int(block_id)

        obj.save()
        return obj

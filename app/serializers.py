from rest_framework import serializers

from .models import Page


class PageListSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="page-detail", lookup_field="pk"
    )

    class Meta:
        model = Page
        fields = ["id", "title", "detail_url"]


class PageDetailSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ["id", "title", "contents"]

    def get_contents(self, obj):
        contents = obj.get_contents()
        return [self._serialize_content(c) for c in contents]

    def _serialize_content(self, content):
        data = {
            'id': content.id,
            'title': content.title,
            'counter': content.counter,
            'type': content.__class__.__name__.lower(),
        }
        base_fields = {'id', 'title', 'counter'}
        fields = content._meta.get_fields()
        for field in fields:
            if field.name in base_fields or field.is_relation:
                continue
            data[field.name] = getattr(content, field.name, None)
        return data

from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import File


class FileSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serialize File Object
    path, name
    """
    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    file_format = serializers.CharField(read_only=True, source="format")

    def get_url(self, obj):
        return obj.path_url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail_path_url


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True, required=True)

    def validate(self, data):
        if data.get('file', None):
            file = File.objects.save_file(
                data.pop('file'),
                allow_formats=['jpg', 'jpeg', 'png', 'xlsx', 'pdf'],
                created_by=self.context['request'].user,
            )
            data['file'] = file
        return data

    def to_representation(self, instance):
        self.fields["file"] = FileSerializer()
        return super().to_representation(instance)


class FilePKRelatedField(serializers.PrimaryKeyRelatedField):

    class Meta:
        label = "file"

    def get_queryset(self):
        now = timezone.now()
        return File.objects.filter(created_at__gte=now - timedelta(hours=3))

from rest_framework import serializers

from motif.models import Motif

__all__ = (
    'MotifListCreateSerializers',
)


class MotifListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motif
        fields = '__all__'

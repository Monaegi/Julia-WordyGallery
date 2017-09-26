from rest_framework import serializers

from motif.models import Motif

__all__ = (
    'MotifListCreateSerializers',
)


class MotifListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motif
        fields = '__all__'

    def validate(self, data):
        name_motif = data.get('name_motif')
        name_art = data.get('name_art')
        if not name_motif:
            raise serializers.ValidationError({
                "detail": "주제를 입력해주세요."
            })
        return data

    def save(self, validated_data):
        motif = Motif.objects.create(
            name_motif=validated_data.get('name_motif'),
            name_art=validated_data.get('name_art')
        )
        return motif
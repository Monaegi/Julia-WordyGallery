from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from art.models import Art, Genre

__all__ = (
    'ArtListSerializers',
)


class ArtListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = '__all__'

        # 장르가 고정될 수 있도록 유효성 검사 설정
        validators = UniqueTogetherValidator(
            queryset=Genre.objects.all(),
            fields=['id', 'name_genre']
        )

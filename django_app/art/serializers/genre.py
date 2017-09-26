from rest_framework import serializers

from ..models import Genre, Art

__all__ = (
    'GenreListSerializers',
)


class GenreListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'pk',
            'name_genre',
        )

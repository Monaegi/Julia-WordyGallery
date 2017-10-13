from django.contrib.auth import get_user_model
from rest_framework import serializers

from art.models import Art
from art.serializers import ArtListSerializers
from ..models import Motif

__all__ = (
    # nested 세부 페이지용
    'MotifDetailSerializers',

    # 조회 / 생성용
    'MotifListCreateSerializers',

    # 수정용
    'MotifUpdateSerializers',
)

User = get_user_model()


class MotifDetailSerializers(serializers.ModelSerializer):
    name_art = ArtListSerializers()

    class Meta:
        model = Motif
        fields = '__all__'


class MotifListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motif
        fields = (
            'name_motif',
            'name_art',
            'motif_author',
        )
        # read_only = (
        #     'name_art',
        #     'motif_author'
        # )

    def validate(self, data):
        name_motif = data.get('name_motif')
        name_art = data.get('name_art')
        motif_author = data.get('motif_author')
        if not name_motif:
            raise serializers.ValidationError({
                "detail": "주제를 입력해주세요."
            })
        elif not name_art:
            raise serializers.ValidationError({
                "detail": "모티프를 생성할 작품을 선택해주세요."
            })
        elif not motif_author:
            raise serializers.ValidationError({
                "detail": "로그인이 필요합니다."
            })
        print('data;@@@@@@@@@@@@@', data)
        return data

    def save(self, *args, **kwargs):
        motif = Motif.objects.create(
            name_motif=self.validated_data['name_motif'],
            name_art=self.validated_data['name_art'],
            motif_author=self.validated_data['motif_author']
        )
        return motif


class MotifUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motif
        fields = '__all__'

        read_only = (
            'name_art',
            'motif_author'
        )
        write_only = (
            'name_art',
            'motif_author',
        )

    def validate(self, data):
        """
        모티프 제목 입력값 검사
        """

        if not data.get('name_motif', None):
            raise serializers.ValidationError({
                "detail": "모티프 제목을 적어주세요."
            })
        if len(data.get('name_motif')) >= 200:
            raise serializers.ValidationError({
                "detail": "200자 이하의 제목을 입력해주세요."
            })
        return data

    def update(self, instance, validated_data):
        """
        변경된 내용으로 저장
        """
        self.instance.name_motif = validated_data['name_motif']
        self.instance.name_art = validated_data['name_art']
        self.instance.motif_author = validated_data['motif_author']
        instance.save()
        return instance


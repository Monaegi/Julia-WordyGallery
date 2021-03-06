from rest_framework import serializers

from ..serializers import MotifDetailSerializers
from ..models import Comment

__all__ = (
    # nested 조회용
    'CommentDetailSerializers',

    # 댓글 생성용
    'CommentListCreateSerializers',

    # 댓글 수정 및 삭제용
    'CommentUpdateDestroySerializers',
)


class CommentDetailSerializers(serializers.ModelSerializer):
    motif = MotifDetailSerializers()

    class Meta:
        model = Comment
        fields = (
            'comment',
            'motif',
        )
        read_only_fields = ('motif',)


class CommentListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'comment',
            'motif',
            'comment_author',
        )

    def validate(self, data):
        motif = data.get('motif')
        comment = data.get('comment')
        comment_author = data.get('comment_author')
        if not motif:
            # 일어날 일이 없지만 혹시나 예외처리
            raise serializers.ValidationError({
                "detail": "모티프 내에서 댓글을 입력하셔야 합니다."
            })
        if not comment:
            raise serializers.ValidationError({
                "detail": "댓글은 최소 1자 이상 입력하셔야 합니다."
            })
        if not comment_author:
            raise serializers.ValidationError({
                "detail": "댓글을 입력하시려면 로그인해주세요."
            })
        return data

    def save(self, *args, **kwargs):
        """
        comment 생성 및 저장
        """
        comment = Comment.objects.create(
            motif=self.validated_data['motif'],
            comment=self.validated_data['comment'],
            comment_author=self.validated_data['comment_author'],
        )
        return comment


class CommentUpdateDestroySerializers(serializers.ModelSerializer):
    """
    comment 수정 및 삭제용
    """
    class Meta:
        model = Comment
        fields = (
            'comment',
            'comment_author',
            'motif',
        )
        # read_only_fields = (
        #     'motif',
        #     'comment_author',
        # )

    def validate(self, data):
        comment = data.get('comment')
        comment_author = data.get('comment_author')
        motif = data.get('motif')
        if not comment:
            raise serializers.ValidationError({
                "detail": "수정할 댓글을 입력하세요."
            })
        print(data)
        return data

    def update(self, instance, validated_data):
        self.instance.comment = validated_data['comment']
        self.instance.comment_author = validated_data['comment_author']
        self.instance.motif = validated_data['motif']
        instance.save()
        return instance


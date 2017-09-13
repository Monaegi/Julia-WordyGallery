from django.db import models

# Create your models here.
# 작품별 주제 모델
from ..art import Art


class Motif(models.Model):
    # 이야기하고 싶은 모티프명
    name_motif = models.CharField(
        max_length=100,
    )
    # 작품명
    name_art = models.ForeignKey(
        Art,
        # on_delete=models.PROTECT,
    )


# 코멘트 저장 모델
class Comment(models.Model):
    # 댓글의 주제
    motif = models.ForeignKey(
        Motif,
        on_delete=models.CASCADE
    )

    # TODO comment 는 텍스트, 이미지 모두 등록 가능하도록 CustomTextField를 생성해야함
    comment = models.TextField()

    # 댓글을 단 사용자
    name_user = models.ForeignKey()

    # 댓글 생성시간
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    # 댓글 수정시간
    date_modified = models.DateTimeField(
        auto_now=True
    )

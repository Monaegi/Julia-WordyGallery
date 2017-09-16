from django.contrib.auth import get_user_model
from django.db import models

__all__ = (
    'Art',
)


# 작품 저장 모델
class Art(models.Model):
    # 작품명
    name_art = models.CharField(
        max_length=100,
    )
    # 작품 이미지
    img_art = models.CharField(
        max_length=500,
    )
    # 아티스트명
    name_artist = models.CharField(
        max_length=100,
    )
    # 작품 정보(연도, 채색방법 등 간결한 정보)
    info_art = models.TextField(
        blank=True,
    )
    # 작품 설명
    text_art = models.TextField(
        blank=True,
    )
    # 댓글
    comment = models.ForeignKey('motif.Comment')


# 작품 분류할 장르 모델
class Genre(models.Model):
    GENRE_TYPE_CHOICES = (
        ('Collage', 'Collage'),
        ('Drawing', 'Drawing'),
        ('Installation', 'Installation'),
        ('New Media', 'New Media'),
        ('Graphic Design', 'Graphic Design'),
        ('Photography', 'Photography'),
        ('Video Art', 'Video Art'),
        ('Print Making', 'Print Making'),
        ('Sculpture', 'Sculpture'),
        ('Others', 'Others'),
    )
    # 장르명
    name_genre = models.CharField(
        max_length=50,
        choices=GENRE_TYPE_CHOICES
    )
    # 작품 id
    art = models.ManyToManyField(
        Art,
        related_name='art',
    )

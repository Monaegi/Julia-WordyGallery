from django.db import models

from utils.fields.custom_imagefields import CustomImageField2

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
    img_art = CustomImageField2(
        max_length=500,
        default='art/default_art.jpg'
    )
    # 아티스트명C
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


# 작품 분류할 장르 모델
class Genre(models.Model):
    GENRE_TYPE_CHOICES = (
        # ('DB에 저장되는 값', '화면에 보이는 값'),
        ('collage', '콜라주'),
        ('drawing', '드로잉'),
        ('installation', '설치미술'),
        ('new-media', '뉴미디어'),
        ('graphic-design', '그래픽디자인'),
        ('photography', '사진'),
        ('video-art', '비디오 아트'),
        ('print-making', '프린팅'),
        ('sculpture', '조각'),
        ('others', '기타'),
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

    def __str__(self, *args, **kwargs):
        return self.name_genre

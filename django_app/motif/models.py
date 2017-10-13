import re
from audioop import reverse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from art.models import Art

# Create your models here.
# 작품별 주제 모델

__all__ = (
    'Motif',
    'Comment',
)

User = get_user_model()


class Motif(models.Model):
    # 이야기하고 싶은 모티프명
    name_motif = models.CharField(
        max_length=100,
    )
    # 작품명
    name_art = models.ForeignKey(
        Art,
        on_delete=models.CASCADE,
    )
    motif_author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name_motif


# 코멘트 저장 모델
class Comment(models.Model):
    # 댓글의 주제
    motif = models.ForeignKey(
        Motif,
        # motif를 삭제하면 comment도 삭제된다.
        on_delete=models.CASCADE
    )

    # comment 컨텐트
    comment = models.TextField()

    # refer_user 활성화용 필드
    html_comment = models.TextField(blank=True)

    # 댓글을 단 사용자
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    # 댓글 생성시간
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    # 댓글 수정시간
    date_modified = models.DateTimeField(
        auto_now=True
    )

    # 댓글 좋아요
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refer_comment_user()

    def refer_comment_user(self):
        p = re.compile(r'(@\w+)')
        user_list = re.findall(p, self.comment)
        ori_comment = self.comment
        for user in user_list:
            user, _ = User.get_object_or_404(name=user.replace('@', ''))
            change_comment = '<a href="{url}" class="refer_user">{user}</a>'.format(
                url=reverse(
                    'member:profile',
                    pk=user.pk,
                    # kwargs={'user': user.replace('@', '')})
                ),
                user=user
            )

            ori_comment = re.sub(r'{}(?![<\w])'.format(
                user),
                change_comment,
                ori_comment,
                count=1
            )

            if not User.objects.filter(name=user).exists():
                return None

            self.html_comment = ori_comment
            super().save(update_fields=['html_comment'])


class CommentLike(models.Model):
    """
    댓글 좋아요 저장 모델
    """
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

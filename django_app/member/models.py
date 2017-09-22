from django.conf import settings
from django.contrib.auth import models as auth_models, get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from utils.fields.custom_imagefields import CustomImageField

### 기본 기능 ###
# 사용자 로그인 - 일반 / 페이스북
# 회원가입
# 로그아웃
# 프로필 정보변경
# 계정탈퇴
###############

__all__ = (
    'MyUser'
)


# 커스텀 사용자 생성 매니저
class MyUserManager(BaseUserManager):
    # 일반사용자 생성 메서드
    def create_user(self, username, name, email=None, password=None, **extra_fields):
        try:
            user = self.model(
                user_type=User.USER_TYPE_DJANGO,
                username=username,
                name=name,
                email=email if email else "",
            )
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            user.set_password(password)
            user.is_active = True
            user.save()
            return user
        except ValidationError:
            raise ValidationError({'detail': 'Enter a proper Email Account'})

    # 관리자 생성 메서드
    def create_superuser(self, username, name, email=None, password=None, **extra_fields):
        try:
            superuser = self.create_user(
                user_type=User.USER_TYPE_DJANGO,
                username=username,
                name=name,
                password=password,
            )
            superuser.is_admin = True
            superuser.is_superuser = True
            superuser.is_active = True
            superuser.save()
            return superuser
        except ValidationError:
            raise ValidationError({"detail": "Enter a proper Email Account"})


# 전체서비스 내 커스텀유저 모델
class MyUser(AbstractBaseUser):
    # 장고, 페이스북 로그인 타입 선택하는 필드.
    USER_TYPE_DJANGO = 'django'
    USER_TYPE_FACEBOOK = 'facebook'
    USER_TYPE_CHOICES = (
        ('django', 'Basic Login'),
        ('facebook', 'Facebook Login'),
    )

    # 장고, 페이스북 로그인 유저를 구분하는 필드
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=USER_TYPE_DJANGO,
    )

    # 회원가입시 입력한 사용자의 ID
    username = models.CharField(
        max_length=100,
        unique=True
    )

    # 사용자의 이름을 저장하는 필드. 회원가입시 등록
    name = models.CharField(
        max_length=100,
    )

    # 사용자의 이메일을 저장하는 필드. 페이스북 사용자용
    email = models.EmailField(default="")

    # 사용자 프로필이미지를 저장하는 필드.
    # TODO CustomImageField 설정 필요
    img_profile = CustomImageField(
        upload_to='member',
        default='member/basic_profile.png',
        blank=True
    )

    # AbstractBaseUser를 상속받음으로써 정의해줘야하는 bool 필드들
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # custom manager 설정
    objects = MyUserManager()

    EMAIL_FIELD = 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.name if self.name else self.username

    @property
    def is_staff(self):
        """일반 사용자 or 스태프 권한"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """user가 주어진 app_label에 해당하는 권한이 있는지, has_perm과 비슷"""
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)

    # 커스텀 수정 퍼미션 메서드용
    def has_edit_perm(self, perm, obj=None):
        if self.pk == obj.pk:
            return True
        return auth_models._user_has_perm(self, perm, obj)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_perm(self, perm, obj)

    # AbstractBaseUser에는 존재하지 않으므로 따로 선언해줌.
    def user_permissions(self):
        return self._user_permissions

    # 장고 admin 이름출력시 필요한 메서드. AbstractBaseUser에는 없어서 따로 정의해줌.
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


User = get_user_model()


# 장고 로그인용 토큰 생성 메서드.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


### 기본 기능 ###
# 사용자 로그인
# 회원가입
# 로그아웃
# 프로필 정보변경
# 계정탈퇴
###############


# 사용자 생성 매니저
class MyUserManager(BaseUserManager):
    # 일반사용자 생성 메서드
    def create_user(self, *args, **kwargs):
        pass

    # 관리자 생성 메서드
    def create_superuser(self, *args, **kwargs):
        pass


# 서비스 내 유저 모델
class MyUser(AbstractBaseUser):
    # 장고, 페이스북 로그인 타입 선택하는 필드.
    USER_TYPE_CHOICES = (
        ('django', '일반 로그인'),
        ('facebook', '페이스북 로그인'),
    )

    # USERNAME_FIELD = ['username',]

    # 장고, 페이스북 로그인 유저를 구분하는 필드
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
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

    # 사용자 프로필이미지를 저장하는 필드.
    img_profile = models.CharField()

    # 사용자 이메일 주소를 등록하는 필드. 페이스북 로그인시 필요
    email = models.CharField(
        max_length=100
    )

    # AbstractBaseUser를 상속받음으로써 정의해줘야하는 bool 필드들
    is_staff = models.BooleanField()
    is_admin = models.BooleanField()
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()

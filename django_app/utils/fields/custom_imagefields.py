from django.db.models.fields.files import ImageFieldFile, ImageField


class CustomImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            # 뒷부분의 쿼리스트링 정보는 나누고 앞부분만 가져오도록 처리함.
            return super().url.split('?')[0]
        except ValueError:
            from django.contrib.staticfiles.storage import staticfiles_storage
            return staticfiles_storage.url(self.fields.static_image_path.split('?')[0])


class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile

    def __init__(self, *args, **kwargs):
        self.static_dir = kwargs.pop(
            'static_image_path',
            'member/basic_profile.png'
        )
        super().__init__(*args, **kwargs)


class CustomImageField2(ImageField):
    attr_class = CustomImageFieldFile

    def __init__(self, *args, **kwargs):
        self.static_dir = kwargs.pop(
            'static_image_path',
            'art/default_art.jpg'
        )
        super().__init__(*args, **kwargs)

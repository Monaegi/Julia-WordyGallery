from django.contrib import admin

# Register your models here.
from .models import Motif, CommentLike, Comment

admin.site.register(Motif)
admin.site.register(Comment)
admin.site.register(CommentLike)
from rest_framework import permissions

__all__ = (
    "IsMotifOwnerOrReadOnly",
)


class IsMotifOwnerOrReadOnly(permissions.BasePermission):
    """
    관리자 또는 자기자신일 경우 perm = True
    또는 obj의 소유자가 요청을 보낸 사용자일 경우 perm = True
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
                permissions.IsAdminUser:
            return True
        return obj.motif_author == request.user


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    관리자 또는 자기자신일 경우 perm = True
    또는 obj의 소유자가 요청을 보낸 사용자일 경우 perm = True
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
                permissions.IsAdminUser:
            return True
        return obj.comment_author == request.user

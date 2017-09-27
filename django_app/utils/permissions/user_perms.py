from rest_framework import permissions


__all__ = (
    'IsOwnerOrReadOnly',
    'ObjectIsRequestUser',
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    관리자 또는 자기자신일 경우 perm = True
    또는 obj의 소유자가 요청을 보낸 사용자일 경우 perm = True
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
                permissions.IsAdminUser:
            return True
        return obj.owner == request.user


class ObjectIsRequestUser(permissions.BasePermission):
    """
    객체 자체가 요청을 보낸 사용자이면 perm = True
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

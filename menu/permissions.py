from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAuthenticated


class IsOwnerOrStaffOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff or request.user.is_superuser


class IsOwnerOrStaffOrAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff or request.user.is_superuser

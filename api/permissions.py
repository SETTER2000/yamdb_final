from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class PermissonForRole(BasePermission):
    """Custom permissons for all models.

    All availiable methods in SETTINGS.ROLES_PERMISSIONS.
    Needed permisson for each ViewSet passed by argument of this class like:

    permissons_clases=[ROLES_PERMISSIONS.get("Genres")]
    """

    def __init__(self, roles_permissions) -> None:
        super().__init__()
        self.roles_permissions = roles_permissions

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in self.roles_permissions[request.user.role]
            )
        return request.method in self.roles_permissions["anon"]

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in self.roles_permissions[request.user.role]
            )
        return request.method in self.roles_permissions["anon"]

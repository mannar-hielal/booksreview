from rest_framework import permissions


class IsOwnProfileOrReadOnly(permissions.BasePermission):
    # the profile owner only can edit
    # if method is get, then return the object read only
    # if method is post or update, check if the object user is equal to logged-in user
    # if yes return true
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    # the user_profile only can edit (the owner of this status)
    # if method is get, then return the object read only
    # if method is post or update, check if the object user_profile as  request.user.profile
    # if yes return true
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile == request.user.profile

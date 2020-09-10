from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # will return true if the user is admin
        # or the http verb is among get,head,option
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    # the review_author only can edit
    # if method is get, then return the object read only
    # if method is post, set review_author as logged-in user
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_author == request.user

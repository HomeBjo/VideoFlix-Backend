from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit it.

    This permission class ensures that:
    - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any user (read-only access).
    - Any modification (POST, PUT, DELETE, etc.) is only allowed for the owner of the object.

    Methods:
    --------
    - has_object_permission(request, view, obj):
        Checks if the request method is a safe method. If so, allows the action.
        If it's a write method, ensures the user making the request is the owner (creator) of the object.
    
    Returns:
    --------
    - True if the request is read-only or if the request is made by the object's owner.
    - False otherwise.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determines if the request should be granted object-level permission.
        
        Args:
        -----
        request (Request): The current request being processed.
        view (View): The view being accessed.
        obj (Model): The object being accessed.

        Returns:
        --------
        bool: True if the request is safe or the user is the object owner, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
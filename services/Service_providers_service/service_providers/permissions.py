from rest_framework import permissions, status
from rest_framework.response import Response
import requests

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow any user to view objects,
    but only staff members to create and get objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow any user to view objects for safe methods (GET, HEAD, OPTIONS).
            return True

        # CHCK IF USER-TOKEN NOT IN HEADERS 
        # Check if user-token is in headers
        if 'User-Token' not in request.headers:
            return False
        
        auth_header = request.headers.get('User-Token')
        
        response = requests.get('http://127.0.0.1:8001/api/userinfo/', headers={'Authorization': auth_header})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            current_user = response.json()
            # Check if the user is staff.
            if current_user.get('is_staff', False):
                # Allow staff members to create and get objects.
                return True
            else:
                # Deny access for non-staff members trying to create or get objects.
                return False
        else:
            # If failed to fetch user information, deny access.
            return False


class IsStaff(permissions.BasePermission):
    """
    Custom permission to only allow staff members to do something.
    """
    def has_permission(self, request, view):
        if 'User-Token' not in request.headers:
            return False
        
        auth_header = request.headers.get('User-Token')
        
        response = requests.get('http://127.0.0.1:8001/api/userinfo/', headers={'Authorization': auth_header})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            current_user = response.json()
            # Check if the user is staff.
            if current_user.get('is_staff', False):
                # Allow staff members to create and get objects.
                return True
            else:
                # Deny access for non-staff members trying to create or get objects.
                return False
        else:
            # If failed to fetch user information, deny access.
            return False

class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'User-Token' not in request.headers:
            return False

        auth_header = request.headers.get('User-Token')

        response = requests.get('http://127.0.0.1:8001/api/userinfo/', headers={'Authorization': auth_header})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return True

        return False

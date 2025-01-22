from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def admin_login(request):
    """
    Admin login to authenticate and return a token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user and user.is_staff:  # Only allow staff/admin users
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)
    return Response({"error": "Invalid credentials or not an admin"}, status=401)




@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Apply the permission class
def admin_logout(request):
    """
    Admin logout to delete the token.
    """
    request.auth.delete()
    return Response({"message": "Logged out successfully"}, status=200)

import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout


@require_POST
@csrf_exempt
def sign_in(request):
    json_data = json.loads(request.body)
    username = json_data["username"]
    password = json_data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        data = {
            "username": username,
            "email": user.email,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)


@require_POST
@csrf_exempt
def sign_out(request):
    logout(request)
    return JsonResponse({"message": "You have been logged out."}, status=200)

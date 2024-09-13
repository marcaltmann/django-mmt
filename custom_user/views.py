import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.utils.translation.trans_real import parse_accept_lang_header
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Profile

User = get_user_model()


def get_preferred_language(request) -> str:
    result = "en"
    langs = parse_accept_lang_header(request.headers.get('Accept-Language'))
    for lang in reversed(langs):
        loc = lang[0][:2]
        if loc == "en" or loc == "de":
            result = loc

    return result


@require_GET
def user(request):
    current_user = request.user
    profile = current_user.profile

    if current_user.is_authenticated:
        return JsonResponse({
            "username": current_user.username,
            "email": current_user.email,
            "locale": profile.locale,
            "admin": current_user.is_superuser,
            "can_upload": True,
        })
    else:
        return JsonResponse({
            "error": "You are not logged in.",
        }, status=401)


@require_POST
@csrf_exempt
def sign_in(request):
    json_data = json.loads(request.body)
    username = json_data["username"]
    password = json_data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        profile = user.profile
        data = {
            "username": username,
            "email": user.email,
            "locale": profile.locale,
            "admin": user.is_superuser,
            "can_upload": True,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)


@require_POST
@csrf_exempt
def register(request):
    json_data = json.loads(request.body)
    username = json_data["username"]
    email = json_data["email"]
    password = json_data["password"]

    if not username:
        return JsonResponse({"error": "Username is required."}, status=400)

    if not email:
        return JsonResponse({"error": "Email is required."}, status=400)

    if not password:
        return JsonResponse({"error": "Password is required."}, status=400)

    try:
        user = User.objects.create_user(username, email, password)
    except IntegrityError:
        return JsonResponse({"error": "Username already taken."}, status=400)

    locale = get_preferred_language(request)
    profile = Profile.objects.create(user=user, locale=locale)

    # create_user_directories(username)
    # send_mail_to_admins()

    return JsonResponse({
        "username": username,
        "email": email,
    }, status=201)


@require_POST
@csrf_exempt
def sign_out(request):
    logout(request)
    return JsonResponse({"message": "You have been logged out."}, status=200)


@require_POST
@csrf_exempt
@login_required()
def update(request):
    user = request.user
    profile = user.profile

    json_data = json.loads(request.body)
    locale = json_data["locale"]

    if locale is None:
        return JsonResponse({"error": "Locale is required."}, status=400)

    if locale not in ["en", "de"]:
        return JsonResponse({"error": "Invalid locale"}, status=400)

    profile.locale = locale
    profile.save()

    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "locale": profile.locale,
    }, status=200)

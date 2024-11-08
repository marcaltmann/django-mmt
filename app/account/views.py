from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.translation.trans_real import parse_accept_lang_header

from account.forms import RegisterForm
from account.models import Profile
from account.tasks import send_new_user_email, send_user_activation_email
from uploaded_files.filesystem import create_user_directories


User = get_user_model()


def get_preferred_language(request) -> str:
    result = "en"
    langs = parse_accept_lang_header(request.headers.get("Accept-Language"))
    for lang in reversed(langs):
        loc = lang[0][:2]
        if loc == "en" or loc == "de":
            result = loc

    return result


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            locale = get_preferred_language(request)
            Profile.objects.create(user=user, locale=locale)
            create_user_directories(user.username)
            send_new_user_email.delay(user.id)

            return redirect("account:registration_complete")
        else:
            pass
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "account/register.html", context)


def registration_complete(request):
    return render(request, "account/registration_complete.html")


@login_required()
def profile(request):
    return render(request, "account/profile.html")

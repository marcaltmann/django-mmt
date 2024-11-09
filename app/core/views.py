from django.shortcuts import render


def welcome(request):
    user = request.user

    return render(request, "core/welcome.html")

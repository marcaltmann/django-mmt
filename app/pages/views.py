from django.shortcuts import render


def welcome(request):
    return render(request, "pages/welcome.html")


def legal_notice(request):
    return render(request, "pages/legal_notice.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def accessibility(request):
    return render(request, "pages/accessibility.html")


def contact(request):
    return render(request, "pages/contact.html")

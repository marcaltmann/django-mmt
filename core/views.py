from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from .models import UploadedFile


@require_GET
@login_required
def my_uploads(request):
    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user)
    data = serializers.serialize("json", uploaded_files)
    return HttpResponse(data, content_type="application/json")

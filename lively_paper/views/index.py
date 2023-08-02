from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@require_GET
def static(request: HttpRequest):
    return render(request=request, template_name=request.path[1:], content_type='application/javascript')

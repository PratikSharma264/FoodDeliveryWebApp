from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def api_overview(request):
    api_overview = {
        "Topic": "This is api overview"
    }
    return Response(api_overview)
# Create your views here.

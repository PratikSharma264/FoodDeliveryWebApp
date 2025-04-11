from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    api_urls = {
        'Topic': "This is your api Overview",
    }
    return Response(api_urls)

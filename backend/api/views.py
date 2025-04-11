from django.shortcuts import render


def api_overview(request):
    api_urls = {
        'API': {
            'API overview': "/api/",
            'API token': "/api/token/",
            'API token refresh': "/api/token/refresh",
        },
        'Merchant': {
            'Register Merchant': "/api/merchant/register/",
        }
    }
    return render(request, 'api/api_overview.html', {'api_urls': api_urls})

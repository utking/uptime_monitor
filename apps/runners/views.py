from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.conf import settings


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def run_checks(request):
    default_check_interval = settings.DEFAULT_CHECK_INTERVAL
    # for every check, pull its schedule and run if it is time
    print('run host checks')
    # __check_hosts(default_check_interval)
    print('run service checks')
    # __check_services(default_check_interval)
    return JsonResponse({'status': 'Ok', 'datetime': str(datetime.now())})

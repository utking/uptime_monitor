from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from apps.helpers.HttpConfigCheck import GenericConfigCheck
from apps.helpers.emails import EmailSender
from apps.checks.models import CheckConfig, CheckHistory
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.conf import settings
from yaml import dump, load
from datetime import datetime


def index(request):
    items = CheckConfig.objects.order_by('name').all()
    return render(request, 'checks/index.html', {'items': items, 'title': 'Service check definitions'})


def location(request, loc):
    items = CheckConfig.objects.filter(location=loc).order_by('name').all()
    return render(request, 'checks/index.html', {'items': items, 'title': 'Checks'})


def view(request, item_id):
    item = get_object_or_404(klass=CheckConfig, id=item_id)
    item_config = dump(item.config.get('flow'))
    return render(request, 'checks/view.html', {'item': item, 'config': item_config, 'title': 'Check details'})


def view_json(request, item_id):
    item = get_object_or_404(klass=CheckConfig, id=item_id)
    item = model_to_dict(item)
    item['flow'] = item['flow']
    item['created_at'] = True
    item['tags'] = ','.join(item['config']['tags'])
    return JsonResponse(item)


def run_checks(check_id: str = None):
    print('Running the check...', check_id)
    if check_id is None:
        items = CheckConfig.objects.all()
    else:
        items = CheckConfig.objects.filter(id=check_id).all()

    if len(items) > 0:
        notifications = EmailSender()
        for item in items:
            try:
                if not GenericConfigCheck(check=item).run():
                    raise Exception('Failed')
            except:
                latest_run = None
                latest_items = CheckHistory.objects.raw(
                    '''SELECT * FROM checks_checkhistory GROUP BY check_id 
                        HAVING created_at = max(created_at) and check_id="{}"'''.format(item.id))
                if latest_items is not None and len(latest_items) > 0:
                    latest_run = latest_items[0]
                if latest_run is not None:
                    notifications.send_email('user@email.localhost',
                                             {
                                                 'check_name': latest_run.name,
                                                 'trace': latest_run.result,
                                                 'status': latest_run.success,
                                                 'resp_code': latest_run.resp_code,
                                                 'created_at': latest_run.created_at,
                                             })
                return False
    else:
        raise Exception('No checks to run')
    return True


@csrf_exempt
@require_http_methods(['GET'])
def get_flow_items(request):
    return JsonResponse(settings.UI_ELEMENTS)


def create(request, item_id: int = None):
    if item_id is not None:
        item = get_object_or_404(klass=CheckConfig, id=item_id)
        title = 'Edit a check'
    else:
        item = None
        title = 'Create a new check'
    return render(request, 'checks/create.html', {'title': title, 'item': item, 'id': item_id})


def delete(request, item_id):
    item = get_object_or_404(klass=CheckConfig, id=item_id)
    item.delete()
    return redirect('/checks')


@csrf_exempt
@require_http_methods(['POST', 'PUT'])
def update(request):
    req_params = load(request.body)
    item_id = req_params.get('id', '').strip()
    name = req_params.get('name', '').strip()
    loc = req_params.get('location', '').strip()
    tags = req_params.get('tags')
    flow = load(req_params.get('flow', '{}'))
    verbose = req_params.get('verbose', False)
    config = {
        'id': item_id,
        'name': name,
        'location': loc,
        'flow': flow,
        'tags': tags,
        'verbose': verbose,
    }

    if request.method == 'POST':
        print('Creating a new check')
        existing = CheckConfig.objects.filter(id=item_id).first()
        if existing is not None:
            return HttpResponse('A check with the ID "{}" already exists'.format(item_id), status=500)
        item = CheckConfig(id=item_id, name=name, location=loc,
                           flow=flow, config=config, created_at=datetime.now())
    elif request.method == 'PUT':
        print('Updating an existing check')
        item = CheckConfig.objects.filter(id=item_id).first()
        if item is None:
            return HttpResponse('A check with the ID "{}" is not found to update'.format(item_id), status=500)
        item.name = name
        item.flow = flow
        item.config = config
        item.location = loc
        item.created_at = datetime.now()
    else:
        return HttpResponse('Wrong method', status=500)

    try:
        is_empty(item_id, 'Check ID')
        is_empty(name, 'Check name')
        is_empty(loc, 'Check location')
        is_empty(flow, 'Check flow')

        item.save()
    except Exception as ex:
        return HttpResponse(str(ex), status=500)
    return JsonResponse({'error': None, 'item': model_to_dict(item)})


def is_empty(item: str, title: str):
    if item is None or not item:
        raise Exception('{} cannot be empty'.format(title))

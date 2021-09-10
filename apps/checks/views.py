from django.shortcuts import render, get_object_or_404, redirect
from apps.helpers.ChecksLoader import ChecksLoader
from apps.helpers.HttpConfigCheck import HttpConfigCheck, GenericConfigCheck
from apps.checks.models import CheckConfig
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.conf import settings
from yaml import dump


def index(request):
    items = CheckConfig.objects.order_by('name').all()
    return render(request, 'checks/index.html', {'items': items, 'title': 'Checks'})


def location(request, loc):
    items = CheckConfig.objects.filter(location=loc).order_by('name').all()
    return render(request, 'checks/index.html', {'items': items, 'title': 'Checks'})


def checks_json(request):
    checks = CheckConfig.objects.order_by('name').all()
    items = []
    for check in checks:
        items.append(model_to_dict(check))
    return JsonResponse({'items': items})


def view(request, item_id):
    item = get_object_or_404(klass=CheckConfig, id=item_id)
    item_config = dump(item.config['flow'])
    return render(request, 'checks/view.html', {'item': item, 'config': item_config, 'title': 'Check details'})


def view_json(request, item_id):
    item = get_object_or_404(klass=CheckConfig, name=item_id)
    return JsonResponse({'item': model_to_dict(item)})


def reload_checks(save=True):
    base_path = settings.CONFIG_BASE_PATH / 'checks'
    loader = ChecksLoader(base_path=base_path)
    items = loader.load()

    if save:
        CheckConfig.objects.all().delete()
        for item in items:
            CheckConfig(id=item['id'], name=item['name'], config=item,
                        location=item['location'], flow=item['flow']).save()
    return items


def run_checks(check_id: int = None):
    if check_id is None:
        items = CheckConfig.objects.all()
    else:
        items = CheckConfig.objects.filter(check_id).all()

    if len(items) > 0:
        for item in items:
            if not GenericConfigCheck(check=item).run():
                return False
    return True


def reload_config(request):
    reload_config_json(request)
    return redirect(index)


def reload_config_json(request):
    reload_checks()
    return JsonResponse({'status': 'OK'})

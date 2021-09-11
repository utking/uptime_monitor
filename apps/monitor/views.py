from django.shortcuts import render, get_object_or_404, redirect
from apps.checks.models import CheckHistory


def index(request):
    return redirect(to='latest')


def overview(request):
    return render(request, 'monitor/overview.html', {'title': 'Checks Overview', 'items': []})


def history(request):
    return render(request, 'monitor/history.html', {'title': 'Checks History', 'items': []})


def latest(request):
    items = CheckHistory.objects.raw(
        'select * from checks_checkhistory group by name having created_at = max(created_at)')

    return render(request, 'monitor/index.html', {'title': 'Latest Checks', 'items': items})


def view(request, item_id):
    item = get_object_or_404(klass=CheckHistory, id=item_id)
    return render(request, 'monitor/view.html', {'title': 'Check details', 'item': item})


def history(request, item_name):
    items = CheckHistory.objects.filter(name=item_name).order_by('-created_at').all()
    return render(request, 'monitor/index.html', {'title': 'Check History for "{}"'.format(item_name), 'items': items})

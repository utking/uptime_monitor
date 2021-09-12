from django.shortcuts import render, get_object_or_404, redirect
from apps.checks.models import CheckHistory, CheckConfig
from apps.checks.views import run_checks
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart


def index(request):
    return redirect(to='latest')


def overview(request):
    return render(request, 'monitor/overview.html', {'title': 'Checks Overview', 'items': []})


def latest(request):
    items = CheckHistory.objects.raw(
        'select * from checks_checkhistory group by name having created_at = max(created_at)')

    return render(request, 'monitor/index.html', {'title': 'Latest Checks', 'items': items})


def view(request, item_id):
    item = get_object_or_404(klass=CheckHistory, id=item_id)
    return render(request, 'monitor/view.html', {'title': 'Check details', 'item': item})


def history(request, item_id):
    item = get_object_or_404(klass=CheckConfig, id=item_id)
    resp_times = CheckHistory.objects.values(
        'success', 'timings', 'created_at'
    ).filter(check_id=item_id).order_by('-created_at')[:100]
    data_timing = [['DateTime', 'Timing']]
    for resp_item in resp_times:
        data_timing.append([resp_item['created_at'], resp_item['timings'][2]])
    data_source = SimpleDataSource(data=data_timing)
    chart_timings = LineChart(data_source, width='100%', html_id='chart_timings')
    items = CheckHistory.objects.filter(check_id=item_id).order_by('-created_at').all()
    return render(request, 'monitor/index.html', {
        'title': 'Check History for "{}"'.format(item.name), 'items': items,
        'chart_timings': chart_timings})


def run(request, item_id):
    get_object_or_404(klass=CheckConfig, id=item_id)
    try:
        run_checks(check_id=item_id)
        return redirect('/monitor/history/{}'.format(item_id))
    except Exception as e:
        print(e)
        return redirect('/monitor/history/{}'.format(item_id))

import datetime
from django.shortcuts import render, get_object_or_404, redirect
from apps.schedule.models import ScheduleItem
from apps.checks.models import CheckConfig
from apscheduler.triggers.cron import CronTrigger
from apps.helpers.ScheduleStore import ScheduleStore
from apps.checks.views import run_checks


def index(request):
    items = ScheduleItem.objects.all()
    return render(request, 'schedule/index.html', {'title': 'Checks schedules', 'items': items})


def update(request):
    item = None
    item_id = request.POST.get('id')
    name = request.POST.get('name')
    check_id = request.POST.get('check_id')
    schedule = request.POST.get('schedule')
    title = ''

    if item_id is not None:
        item = ScheduleItem.objects.filter(id=item_id).first()
        title = 'Edit a check schedule'
    if item is None:
        item = ScheduleItem()
        title = 'Create a check schedule'

    item.name = name.strip()
    item.check_id_id = check_id
    item.schedule = schedule
    item.created_at = datetime.datetime.now()

    try:
        if name is None or not name.strip():
            raise Exception('The name cannot be empty')
        if CheckConfig.objects.filter(id=check_id).first() is None:
            raise Exception('The selected check cannot be found')
        item.save()
        populate_schedule()
    except Exception as ex:
        checks = CheckConfig.objects.all()
        return render(request, 'schedule/create.html', {'title': title, 'item': item, 'checks': checks, 'error': ex})
    return redirect('/schedule/view/{}'.format(item.id))


def create(request, item_id: int = None):
    checks = CheckConfig.objects.all()
    if item_id is not None:
        item = get_object_or_404(klass=ScheduleItem, id=item_id)
        title = 'Edit a check schedule'
    else:
        item = None
        title = 'Create a check schedule'
    return render(request, 'schedule/create.html', {'title': title, 'item': item, 'checks': checks})


def view(request, item_id):
    item = get_object_or_404(klass=ScheduleItem, id=item_id)
    return render(request, 'schedule/view.html', {'title': 'Check schedule details', 'item': item})


def delete(request, item_id):
    item = get_object_or_404(klass=ScheduleItem, id=item_id)
    item.delete()
    populate_schedule()
    return redirect('index')


def run_check_job(arg):
    run_checks(arg)


def populate_schedule():
    print('Creating a scheduler and adding the check jobs in it')
    items = ScheduleItem.objects.all()
    scheduler = ScheduleStore.get_instance().get_scheduler()
    scheduler.remove_all_jobs()
    for item in items:
        print('Creating "{}" running by cron "{}"'.format(item.check_id, item.schedule))
        trigger = CronTrigger().from_crontab(item.schedule)
        scheduler.add_job(run_check_job, trigger=trigger, id=item.check_id.id, args=[item.check_id.id],
                          max_instances=1, replace_existing=True)
    print('Schedules are ready')

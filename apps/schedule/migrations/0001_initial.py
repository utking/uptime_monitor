# Generated by Django 3.1.3 on 2021-09-11 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('schedule', models.CharField(default='* * * * *', max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('check_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='checks.checkconfig')),
            ],
        ),
        migrations.AddIndex(
            model_name='scheduleitem',
            index=models.Index(fields=['check_id'], name='schedule_sc_check_i_66791f_idx'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-10-08 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20201017_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowrun',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='constantvalue',
            name='value',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='flowrunschedule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='node',
            name='function',
            field=models.CharField(choices=[('filter', 'Filter'), ('math_expression', 'Math expression'), ('summarize', 'Summarize'), ('http_get_request', 'Http Request'), ('parse_csv', 'Parse CSV')], max_length=40),
        ),
        migrations.AlterField(
            model_name='noderun',
            name='function',
            field=models.CharField(choices=[('filter', 'Filter'), ('math_expression', 'Math expression'), ('summarize', 'Summarize'), ('http_get_request', 'Http Request'), ('parse_csv', 'Parse CSV')], max_length=40),
        ),
        migrations.AlterField(
            model_name='noderun',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='noderunextraoutput',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value',
            field=models.JSONField(),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
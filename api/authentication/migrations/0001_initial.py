# Generated by Django 3.2.7 on 2022-01-04 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('service', models.CharField(choices=[('slack', 'Slack'), ('google_sheets', 'Google Sheets'), ('postgresql', 'Postgresql'), ('sqlite', 'SQLite'), ('mysql', 'MySQL')], max_length=50)),
                ('credentials', models.JSONField(default=dict)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_authentication.credentials_set+', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='DatabaseCredentials',
            fields=[
                ('credentials_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.credentials')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('host', models.CharField(max_length=100)),
                ('port', models.IntegerField()),
                ('database', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Database Credentials',
                'verbose_name_plural': 'Database Credentials',
            },
            bases=('authentication.credentials',),
        ),
        migrations.CreateModel(
            name='OAuth2Credentials',
            fields=[
                ('credentials_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.credentials')),
                ('access_token', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('token', models.JSONField()),
            ],
            options={
                'verbose_name': 'OAuth2 Credentials',
                'verbose_name_plural': 'OAuth2 Credentials',
            },
            bases=('authentication.credentials',),
        ),
    ]
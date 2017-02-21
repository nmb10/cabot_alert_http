# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_http_alert(apps, schema_editor):
    # We can't import the HTTPAlert model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    HTTPAlert = apps.get_model('cabot_alert_http', 'HTTPAlert')
    if not HTTPAlert.objects.exists():
        HTTPAlert.objects.create(title='HTTPAlert')


class Migration(migrations.Migration):

    dependencies = [
        ('cabot_alert_http', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_http_alert),
    ]

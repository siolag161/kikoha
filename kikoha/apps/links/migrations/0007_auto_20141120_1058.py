# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_auto_20141120_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='created',
            field=core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False),
            preserve_default=True,
        ),
    ]

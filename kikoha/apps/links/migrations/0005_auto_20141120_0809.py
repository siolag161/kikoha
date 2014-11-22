# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_auto_20141120_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
            preserve_default=True,
        ),
    ]

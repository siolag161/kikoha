# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141117_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='desc',
            field=models.CharField(max_length=500, null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0005_auto_20141212_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='author',
        ),
        migrations.RemoveField(
            model_name='link',
            name='community',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]

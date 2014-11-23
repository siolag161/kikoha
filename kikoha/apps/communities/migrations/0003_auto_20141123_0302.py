# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_auto_20141123_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='community',
            field=models.ForeignKey(related_name='links', verbose_name='Community', to='communities.Community'),
            preserve_default=True,
        ),
    ]

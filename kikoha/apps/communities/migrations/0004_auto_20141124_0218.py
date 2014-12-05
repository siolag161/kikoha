# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_auto_20141123_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='downvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='score',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='upvotes',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]

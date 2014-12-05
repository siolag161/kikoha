# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadedcomment',
            name='depth',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='numchild',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='path',
            field=models.CharField(default='', unique=True, max_length=255),
            preserve_default=False,
        ),
    ]

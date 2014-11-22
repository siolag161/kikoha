# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_link_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=core.fields.CoreSlugField(max_length=250, null=True, verbose_name='Slug', blank=True),
            preserve_default=True,
        ),
    ]

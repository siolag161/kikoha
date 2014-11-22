# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_remove_link_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20141124_0218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='downvotes',
        ),
        migrations.AddField(
            model_name='link',
            name='totalvotes',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]

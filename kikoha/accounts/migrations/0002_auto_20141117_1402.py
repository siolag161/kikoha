# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='self_desc',
        ),
        migrations.AddField(
            model_name='user',
            name='desc',
            field=models.CharField(default='', max_length=500, verbose_name='description', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='comment_karma',
            field=models.IntegerField(null=True, verbose_name='comment karma', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='link_karma',
            field=models.IntegerField(null=True, verbose_name='link karma', blank=True),
            preserve_default=True,
        ),
    ]

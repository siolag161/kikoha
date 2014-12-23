# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0006_auto_20141215_0234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0.0)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', core.fields.CoreSlugField(db_index=True, max_length=250, null=True, verbose_name='Slug', blank=True)),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('upvotes', models.PositiveIntegerField(default=1)),
                ('totalvotes', models.IntegerField(default=1)),
                ('url', models.URLField()),
                ('author', models.ForeignKey(related_name='links', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
                ('community', models.ForeignKey(related_name='links', verbose_name='Community', to='communities.Community')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

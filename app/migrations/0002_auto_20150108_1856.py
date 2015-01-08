# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='content_background',
            field=redactor.fields.RedactorField(default='', null=True, verbose_name='Background', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='content_conclusion',
            field=redactor.fields.RedactorField(default='', null=True, verbose_name='Conclusion', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='content_revenue',
            field=redactor.fields.RedactorField(default='', null=True, verbose_name='Analysis of Impact on Revenue', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='content_spending',
            field=redactor.fields.RedactorField(default='', null=True, verbose_name='Analysis of Impact on Spending', blank=True),
            preserve_default=True,
        ),
    ]

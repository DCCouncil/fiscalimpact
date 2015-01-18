# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150108_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='fis_type',
            field=models.CharField(choices=[('E', 'Emergency'), ('ANS', 'Amendment in the Nature of a Substitute'), ('R', 'Resolution'), ('A', 'Act'), ('Am', 'Amendment')], default='E', max_length=5),
            preserve_default=True,
        ),
    ]

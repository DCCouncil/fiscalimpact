# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('slug', models.SlugField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('office', models.CharField(choices=[('PM', 'Chairman Phil Mendelson'), ('BN', 'Councilmember Brianne Nadeau'), ('JE', 'Councilmember Jack Evans'), ('MC', 'Councilmember Mary Cheh'), ('KM', 'Councilmember Kenyan McDuffie'), ('CA', 'Councilmember Charles Allen'), ('YA', 'Councilmember Yvette Alexander'), ('VO', 'Councilmember Vincent Orange'), ('AB', 'Councilmember Anita Bonds'), ('DG', 'Councilmember David Grosso'), ('ES', 'Councilmember Elissa Silverman')], default='pm', max_length=400)),
                ('measure_type', models.CharField(choices=[('B', 'Bill'), ('PR', 'Proposed Resolution')], default='B', max_length=5)),
                ('measure_number', models.CharField(null=True, blank=True, max_length=64)),
                ('short_title', models.CharField(null=True, blank=True, max_length=300)),
                ('amendment', models.BooleanField(default=False)),
                ('amendment_number', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('review', 'Review'), ('published', 'Published')], default='draft', max_length=10)),
                ('content_conclusion', redactor.fields.RedactorField(verbose_name='Conclusion')),
                ('content_background', redactor.fields.RedactorField(verbose_name='Background')),
                ('content_revenue', redactor.fields.RedactorField(verbose_name='Analysis of Impact on Revenue')),
                ('content_spending', redactor.fields.RedactorField(verbose_name='Analysis of Impact on Spending')),
                ('publish_date', models.DateField(null=True, blank=True)),
                ('employee', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_publish', 'Can Publish'),),
            },
            bases=(models.Model,),
        ),
    ]

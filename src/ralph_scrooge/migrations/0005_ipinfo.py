# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ralph_scrooge', '0004_auto_20161118_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPInfo',
            fields=[
                ('pricingobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ralph_scrooge.PricingObject')),
                ('number', models.DecimalField(decimal_places=0, default=None, editable=False, help_text='Presented as int.', max_digits=39, unique=True, verbose_name='IP address')),
            ],
            options={
                'abstract': False,
            },
            bases=('ralph_scrooge.pricingobject',),
        ),
    ]

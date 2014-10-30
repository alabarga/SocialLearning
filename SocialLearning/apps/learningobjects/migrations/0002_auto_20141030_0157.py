# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learningobjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='url',
            field=models.URLField(max_length=255),
        ),
    ]

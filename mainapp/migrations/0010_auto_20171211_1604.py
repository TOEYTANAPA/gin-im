# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_qmatrix'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qmatrix',
            old_name='amount',
            new_name='reward',
        ),
        migrations.RemoveField(
            model_name='qmatrix',
            name='frequency',
        ),
    ]
